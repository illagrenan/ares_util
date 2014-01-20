#!/usr/bin/python
# coding=utf-8

import urllib2
import sys
import xmltodict

from .exceptions import InvalidCompanyIDError, AresNoResponseError

ARES_API_URL = 'http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi?ico=%s'


def call_ares(company_id):
    """
    Validate given company_id and fetch data from ARES.

    Example:
    ========
        >>> invalid_company_id = 42
        >>> call_ares(invalid_company_id)
        False

        >>> valid_company_id = 27074358
        >>> returned_dict = call_ares(valid_company_id)
        >>> returned_dict['legal']['company_id'] == valid_company_id
        True

    Run doctest:
    ============
        >>> # python -m doctest .\ares.py

    @param company_id: int 8-digit number
    @return: @raise AresNoResponse:
    """
    try:
        validate_czech_company_id(company_id)
    except InvalidCompanyIDError:
        return False

    response = urllib2.urlopen(ARES_API_URL % company_id)

    if response.getcode() != 200:
        raise AresNoResponseError()

    xml_reponse = response.read()
    ares_data = xmltodict.parse(xml_reponse)

    response_root = ares_data['are:Ares_odpovedi']['are:Odpoved']
    number_of_results = response_root['are:Pocet_zaznamu']

    if int(number_of_results) == 0:
        return False

    company_record = response_root['are:Zaznam']
    address = company_record['are:Identifikace']['are:Adresa_ARES']

    result_company_info = {
        'legal': {
            'company_name': company_record['are:Obchodni_firma'],
            'company_id': int(company_record['are:ICO'])
        },
        'address': {
            'region': address.get('dtt:Nazev_okresu', None),
            'city': address['dtt:Nazev_obce'],
            'city_part': address.get('dtt:Nazev_casti_obce', None),
            'street': address['dtt:Nazev_ulice'] + " " + build_czech_address(address.get('dtt:Cislo_domovni', None), address.get(
                'dtt:Cislo_orientacni', None)),
        }
    }

    return result_company_info


def build_czech_address(house_number, orientation_number):
    """
    https://cs.wikipedia.org/wiki/Ozna%C4%8Dov%C3%A1n%C3%AD_dom%C5%AF

    číslo popisné/číslo orientační
    """
    if not orientation_number:
        return str(house_number)

    return str(house_number) + "/" + str(orientation_number)


def validate_czech_company_id(business_id):
    """
    http://www.abclinuxu.cz/blog/bloK/2008/10/kontrola-ic
    http://latrine.dgx.cz/jak-overit-platne-ic-a-rodne-cislo

    @param business_id:
    @raise ValidationError:
    """
    business_id = str(business_id)

    if len(business_id) != 8:
        raise InvalidCompanyIDError("Company ID must be 8 digits long")

    try:
        digits = map(int, list(business_id.rjust(8, "0")))
    except ValueError:
        raise InvalidCompanyIDError("Company ID must be a number")

    remainder = sum([digits[i] * (8 - i) for i in range(7)]) % 11
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