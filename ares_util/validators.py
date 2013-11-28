# coding=utf-8

from .exceptions import ValidationError


def validate_czech_business_id(business_id):
    """
    http://www.abclinuxu.cz/blog/bloK/2008/10/kontrola-ic
    http://latrine.dgx.cz/jak-overit-platne-ic-a-rodne-cislo

    @param business_id:
    @raise ValidationError:
    """
    business_id = str(business_id)

    if len(business_id) != 8:
        raise ValidationError("IČ musí mít přesně 8 znaků")

    try:
        digits = map(int, list(business_id.rjust(8, "0")))
    except ValueError:
        raise ValidationError("IČ není číslo")

    remainder = sum([digits[i] * (8 - i) for i in range(7)]) % 11
    cksum = {0: 1, 10: 1, 1: 0}.get(remainder, 11 - remainder)
    if digits[7] != cksum:
        raise ValidationError("Špatný kontrolní součet IČ")
