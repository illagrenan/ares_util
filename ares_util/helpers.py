# !/usr/bin/python
# coding=utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

from .settings import COMPANY_ID_LENGTH


def normalize_company_id_length(business_id):
    """
    Normalize given Company ID to 8-digits format.

    Example:
    ========
        >>> company_id = "27074358"
        >>> normalize_company_id_length(company_id) == "27074358"
        True

        >>> company_id = "2707435"
        >>> normalize_company_id_length(company_id) == "02707435"
        True


    :type business_id: unicode
    :rtype: unicode
    """

    return business_id.rjust(COMPANY_ID_LENGTH, "0")
