#!/usr/bin/python
# coding=utf-8

import urllib2
import sys
import xmltodict

ARES_API_URL = 'http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi?ico=%s'


class ValidationError(Exception):
    pass


class AresNoResponse(Exception):
    pass


def call_ares(czech_business_id):
    """
    Foo bar lalala

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

    @param czech_business_id: int 8-digit number
    @return: @raise AresNoResponse:
    """
    try:
        # Save API
        validate_czech_business_id(czech_business_id)
    except ValidationError:
        return False

    response = urllib2.urlopen(ARES_API_URL % czech_business_id)

    if response.getcode() != 200:
        raise AresNoResponse()

    xml_reponse = response.read()
    ares_data = xmltodict.parse(xml_reponse)

    root = ares_data['are:Ares_odpovedi']['are:Odpoved']
    number_of_results = root['are:Pocet_zaznamu']

    if int(number_of_results) == 0:
        return False

    zaznam = root['are:Zaznam']
    adresa = zaznam['are:Identifikace']['are:Adresa_ARES']

    result_company_info = {
        'legal': {
            'company_name': zaznam['are:Obchodni_firma'],
            'business_number': int(zaznam['are:ICO'])
        },
        'address': {
            'region': adresa['dtt:Nazev_okresu'],
            'city': adresa['dtt:Nazev_obce'],
            'city_part': adresa['dtt:Nazev_casti_obce'],
            'street': adresa['dtt:Nazev_ulice'] + " " + adresa['dtt:Cislo_domovni'] + "/" + adresa[
                'dtt:Cislo_orientacni'],
        }
    }

    return result_company_info


def validate_czech_business_id(ico):
    ico = str(ico)

    if len(ico) != 8:
        raise ValidationError("IČ musí mít přesně 8 znaků")

    try:
        digits = map(int, list(ico.rjust(8, "0")))
    except ValueError:
        raise ValidationError("IČ není číslo")

    remainder = sum([digits[i] * (8 - i) for i in range(7)]) % 11
    cksum = {0: 1, 10: 1, 1: 0}.get(remainder, 11 - remainder)
    if digits[7] != cksum:
        raise ValidationError("Špatný kontrolní součet IČ")


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