# coding=utf-8

"""This module is designed only for use with Django."""

from django.core.exceptions import ValidationError

# TODO Add support for Django translations
# from django.utils.translation import ugettext as _

from .ares import call_ares, validate_czech_company_id
from .exceptions import InvalidCompanyIDError


def czech_company_id_numeric_validator(business_id):
    try:
        validate_czech_company_id(business_id)
    except InvalidCompanyIDError, e:
        raise ValidationError(str(e))


def czech_company_id_ares_api_validator(business_id):
    if not call_ares(business_id):
        raise ValidationError("Company ID is not registered in ARES.")