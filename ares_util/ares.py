#!/usr/bin/python
# coding=utf-8

import urllib2
import sys
import xmltodict
from .validators import validate_czech_business_id
from .exceptions import ValidationError, AresNoResponse

ARES_API_URL = 'http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi?ico=%s'


def call_ares(business_id):
    """
    Validate given business_id and fetch data from ARES.

    Example:
    ========
        >>> invalid_business_id = 42
        >>> call_ares(invalid_business_id)
        False

        >>> valid_business_id = 27074358
        >>> returned_dict = call_ares(valid_business_id)
        >>> returned_dict['legal']['business_number'] == valid_business_id
        True

    Run doctest:
    ============
        >>> # python -m doctest .\ares.py

    @param business_id: int 8-digit number
    @return: @raise AresNoResponse:
    """
    try:
        validate_czech_business_id(business_id)
    except ValidationError:
        return False

    response = urllib2.urlopen(ARES_API_URL % business_id)

    if response.getcode() != 200:
        raise AresNoResponse()

    xml_reponse = response.read()
    ares_data = xmltodict.parse(xml_reponse)

    root = ares_data['are:Ares_odpovedi']['are:Odpoved']
    number_of_results = root['are:Pocet_zaznamu']

    if int(number_of_results) == 0:
        return False

    zaznam = root['are:Zaznam']
    address = zaznam['are:Identifikace']['are:Adresa_ARES']

    result_company_info = {
        'legal': {
            'company_name': zaznam['are:Obchodni_firma'],
            'business_number': int(zaznam['are:ICO'])
        },
        'address': {
            'region': address['dtt:Nazev_okresu'],
            'city': address['dtt:Nazev_obce'],
            'city_part': address['dtt:Nazev_casti_obce'],
            'street': address['dtt:Nazev_ulice'] + " " + address['dtt:Cislo_domovni'] + "/" + address[
                'dtt:Cislo_orientacni'],
        }
    }

    return result_company_info


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ('Pass arguments')
        sys.exit(2)

    business_id_to_check = sys.argv[1]
    ares_response = call_ares(business_id_to_check)

    if not ares_response:
        print('Business ID "%s" is not valid' % business_id_to_check)
    else:
        print (ares_response)

    sys.exit(1)