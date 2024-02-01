# !/usr/bin/python
# coding=utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
import re
import sys
from urllib.parse import urljoin

import requests
from requests.status_codes import codes
from requests.exceptions import RequestException

from .exceptions import InvalidCompanyIDError, AresConnectionError, AresServerError
from .helpers import normalize_company_id_length
from .settings import COMPANY_ID_LENGTH, ARES_API_URL


def call_ares(company_id):
    """
    Validate given company_id and fetch data from ARES.

    Example:
    ========
        >>> invalid_company_id = 42
        >>> call_ares(invalid_company_id)
        False

        >>> valid_company_id = u"27074358"
        >>> returned_dict = call_ares(valid_company_id)
        >>> returned_dict['legal']['company_id'] == valid_company_id
        True

    :param company_id: 8-digit number
    :type company_id: str|int
    """
    try:
        company_id = validate_czech_company_id(company_id)
    except InvalidCompanyIDError:
        return False

    try:
        url = urljoin(ARES_API_URL, company_id)
        response = requests.get(url)
    except RequestException as e:
        raise AresConnectionError('Exception, ' + str(e))

    if response.status_code in (codes.bad_request, codes.not_found):
        return False

    response_json = response.json()
    if response.status_code != codes.ok:
        raise AresServerError(response_json["kod"], response_json["popis"])

    address = response_json["sidlo"]
    full_text_address = address.get("textovaAdresa", '')

    result_company_info = {
        'legal': {
            'company_name': response_json.get("obchodniJmeno"),
            'company_id': response_json.get("ico"),
            'company_vat_id': response_json.get("dic"),
            'legal_form': response_json.get("pravniForma"),
            'tax_office': response_json.get("financniUrad"),
            'creation_date': response_json.get('datumVzniku'),
            'update_date': response_json.get('datumAktualizace'),
            'source': response_json.get('primarniZdroj'),
            'sub_register': response_json.get('subRegistrSzr'),
        },
        'address': {
            'state_code': address.get('kodStatu'),
            'state': address.get('nazevStatu'),
            'county_code': address.get('kodKraje'),
            'county': address.get('nazevKraje'),
            'region_code': address.get('kodOkresu'),
            'city_district_part_code': address.get('kodMestskeCastiObvodu'),
            'street_code': address.get('kodUlice'),
            'city_district_part': address.get('nazevMestskeCastiObvodu'),
            'street_name': address.get('nazevUlice'),
            'house_number': address.get('cisloDomovni'),
            'city_part_code': address.get('kodCastiObce'),
            'orientation_number': address.get('cisloOrientacni'),
            'address_id': address.get('kodAdresnihoMista'),
            'full_text_address': full_text_address,
            'address_type': address.get('typCisloDomovni'),
            'standardized_address': address.get('standardizaceAdresy'),
            'region': address.get('nazevOkresu'),
            'city': build_city(address.get('nazevObce'), full_text_address),
            'city_code': address.get('kodObce'),
            'city_part': address.get('nazevCastiObce'),
            'street': build_czech_street(address.get('nazevUlice', ''), address.get('nazevObce'),
                                         address.get('nazevCastiObce'),
                                         address.get('cisloDomovni'),
                                         address.get('cisloOrientacni'), full_text_address),
            'zip_code': get_czech_zip_code(address.get('psc'), full_text_address)
        }
    }
    return result_company_info


def get_czech_zip_code(ares_data, full_text_address):
    """
    :type ares_data: unicode
    :type full_text_address: unicode
    :rtype: unicode
    """
    if isinstance(ares_data, int):
        return ares_data
    if ares_data and ares_data.isdigit():
        return ares_data.strip()

    zip_code_regex = re.compile(r'PS[CČ]?\s+(?P<zip_code>\d+)', re.IGNORECASE | re.UNICODE)
    search = re.search(zip_code_regex, full_text_address)

    if search:
        return search.groupdict()["zip_code"].strip()
    else:
        logging.warning("Cannot retrieve ZIP_CODE from this: \"{0}\" address".format(full_text_address))

        # TODO Improve this code
        return ""


def build_czech_street(street_name, city_name, neighborhood, house_number, orientation_number, full_text_address):
    """
    https://cs.wikipedia.org/wiki/Ozna%C4%8Dov%C3%A1n%C3%AD_dom%C5%AF
    číslo popisné/číslo orientační

    :type street_name: unicode|None
    :type city_name: unicode|None
    :type neighborhood: unicode|None
    :type house_number: int|None
    :type orientation_number: int|None
    :type full_text_address: unicode
    :rtype: unicode
    """
    street_name = street_name or neighborhood or city_name  # Fallback in case of a small village

    if not street_name and not house_number:
        return guess_czech_street_from_full_text_address(full_text_address)

    if not orientation_number:
        return "{0}{1}".format(street_name, " %s" % house_number if house_number else "")

    return "{0} {1}/{2}".format(street_name, str(house_number), str(orientation_number))


def guess_czech_street_from_full_text_address(full_text_address):
    """
    :type full_text_address: unicode
    :rtype: unicode
    """
    address_parts = full_text_address.split(',')

    # Examples:
    #   Ústí nad Labem-město, Vaníčkova 11
    #                         ^^^^^^^^^^^^
    #
    #   Bohutín 310
    #   ^^^^^^^^^^^
    if len(address_parts) < 3:
        # Get the last element of a list
        return address_parts[-1].strip()

    # Examples:
    #   Mohelnice, Družstevní 338/16, PSČ 78985
    #              ^^^^^^^^^^^^^^^^^
    elif len(address_parts) == 3:
        return address_parts[1].strip()
    else:
        logging.warning("Cannot parse this: \"%s\" address" % full_text_address)
        # TODO Improve this code
        return ""


def build_city(city, address):
    """
    :type city: unicode
    :type address: unicode
    :rtype: unicode
    """
    return city or address.split(',')[0].strip()


def validate_czech_company_id(business_id: str) -> str:
    """
    https://www.abclinuxu.cz/blog/bloK/2008/10/kontrola-ic
    https://latrine.dgx.cz/jak-overit-platne-ic-a-rodne-cislo

    :type business_id: str
    :rtype: str
    """

    business_id = normalize_company_id_length(business_id)

    try:
        digits = list(map(int, list(business_id)))
    except ValueError:
        raise InvalidCompanyIDError("Company ID must be a number")

    remainder = sum([digits[i] * (COMPANY_ID_LENGTH - i) for i in range(7)]) % 11
    cksum = {0: 1, 10: 1, 1: 0}.get(remainder, 11 - remainder)
    if digits[7] != cksum:
        raise InvalidCompanyIDError("Wrong Company ID checksum")

    return business_id


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Pass company ID as a function argument')
        sys.exit(2)

    company_id_to_check = sys.argv[1]
    ares_response = call_ares(company_id_to_check)

    if not ares_response:
        print("Company ID \"{0}\" is not valid".format(company_id_to_check))
    else:
        print(ares_response)

    sys.exit(0)
