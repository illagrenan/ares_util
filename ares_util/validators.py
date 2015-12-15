# !/usr/bin/python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import (str)

from django.core.exceptions import ValidationError
# TODO Add support for Django translations
# from django.utils.translation import ugettext as _

from .ares import call_ares, validate_czech_company_id
from .exceptions import InvalidCompanyIDError


def czech_company_id_numeric_validator(business_id):
    """
    :type business_id: unicode
    """

    try:
        validate_czech_company_id(business_id)
    except InvalidCompanyIDError as e:
        raise ValidationError(str(e))


def czech_company_id_ares_api_validator(business_id):
    """
    :type business_id: unicode
    """

    if not call_ares(business_id):
        raise ValidationError("Company ID is not registered in ARES.")
