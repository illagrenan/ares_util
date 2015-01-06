# !/usr/bin/python
# coding=utf-8

from __future__ import unicode_literals

import sys
import urllib
import urllib2
import warnings

import xmltodict

from .settings import ARES_API_URL, COMPANY_ID_LENGTH

from .helpers import normalize_company_id_length
from .exceptions import InvalidCompanyIDError, AresNoResponseError


def call_ares(company_id):
    """
    Validate given company_id and fetch data from ARES.

    Example:
    ========
        >>> invalid_company_id = 42
        >>> call_ares(invalid_company_id)
        False

        >>> valid_company_id = "27074358"
        >>> returned_dict = call_ares(valid_company_id)
        >>> returned_dict['legal']['company_id'] == valid_company_id
        True

    @param company_id: int 8-digit number
    @return: @raise AresNoResponse:
    """
    try:
        validate_czech_company_id(company_id)
    except InvalidCompanyIDError:
        return False

    params = urllib.urlencode({'ico': company_id})
    response = urllib2.urlopen(ARES_API_URL + "?%s" % params)

    if response.getcode() != 200:
        raise AresNoResponseError()

    xml_response = response.read()
    ares_data = xmltodict.parse(xml_response)

    response_root = ares_data['are:Ares_odpovedi']['are:Odpoved']
    number_of_results = response_root['D:PZA']

    if int(number_of_results) == 0:
        return False

    company_record = response_root['D:VBAS']
    address = company_record['D:AA']
    text_address = address.get('D:AT', '')

    result_company_info = {
        'legal': {
            'company_name': get_text_value(company_record.get('D:OF', None)),
            'company_id': get_text_value(company_record.get('D:ICO', None)),
            'company_vat_id': get_text_value(company_record.get('D:DIC', None)),
            'legal_form': get_legal_form(company_record.get('D:PF', None))
        },
        'address': {
            'region': address.get('D:NOK', None),
            'city': build_city(address.get('D:N', None), text_address),
            'city_part': address.get('D:NCO', None),
            'street': build_czech_street(address.get('D:NU', str()), address.get('D:N', None),
                                         address.get('D:NCO', None), address.get('D:CD', None),
                                         address.get('D:CO', None), text_address),
            'zip_code': address.get('D:PSC', None)
        }
    }
    return result_company_info


def get_text_value(node):
    return node.get('#text', None) if node else None


def build_czech_street(street_name, city_name, neighborhood, house_number, orientation_number, address):
    """
    https://cs.wikipedia.org/wiki/Ozna%C4%8Dov%C3%A1n%C3%AD_dom%C5%AF

    číslo popisné/číslo orientační
    """
    street_name = street_name or neighborhood or city_name  # Fallback in case of a small village

    if not street_name or not house_number:
        return address.split(',')[-1].strip()

    if not orientation_number:
        return street_name + ' ' + str(house_number)

    return street_name + ' ' + str(house_number) + "/" + str(orientation_number)


def build_city(city, address):
    return city or address.split(',')[0].strip()


def get_legal_form(legal_form):
    """
    http://wwwinfo.mfcr.cz/ares/aresPrFor.html.cz

    @param legal_form:
    @return:
    """
    if legal_form:
        return legal_form.get('D:KPF', None)

    return None


def validate_czech_company_id(business_id):
    """
    http://www.abclinuxu.cz/blog/bloK/2008/10/kontrola-ic
    http://latrine.dgx.cz/jak-overit-platne-ic-a-rodne-cislo

    @param business_id: str
    @raise ValidationError:
    """

    if isinstance(business_id, int):
        warnings.warn("In version 0.1.5 integer parameter will be invalid. "
                      "Use string instead.", DeprecationWarning, stacklevel=2)

    business_id = unicode(business_id)

    # if len(business_id) != 8:
    # raise InvalidCompanyIDError("Company ID must be 8 digits long")

    try:
        digits = map(int, list(normalize_company_id_length(business_id)))
    except ValueError:
        raise InvalidCompanyIDError("Company ID must be a number")

    remainder = sum([digits[i] * (COMPANY_ID_LENGTH - i) for i in range(7)]) % 11
    cksum = {0: 1, 10: 1, 1: 0}.get(remainder, 11 - remainder)
    if digits[7] != cksum:
        raise InvalidCompanyIDError("Wrong Company ID checksum")

    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ('Pass company ID as a function argument')
        sys.exit(2)

    company_id_to_check = sys.argv[1]
    ares_response = call_ares(company_id_to_check)

    if not ares_response:
        print('Company ID "%s" is not valid' % company_id_to_check)
    else:
        print (ares_response)

    sys.exit(1)
