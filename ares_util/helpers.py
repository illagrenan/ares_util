# !/usr/bin/python
# coding=utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

from .settings import COMPANY_ID_LENGTH


def normalize_company_id_length(business_id: str) -> str:
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


    :type business_id: str
    :rtype: str
    """

    return str(business_id).zfill(COMPANY_ID_LENGTH)


def is_record_active(record: dict):
    """
    Validate record being active

    Example:
    ========
        >>> data = {"datumZapisu": "2020-01-01", "datumVymazu": "2022-01-01"}
        >>> is_record_active(data)
        False

        >>> data = {"datumZapisu": "2020-01-01"}
        >>> is_record_active(data)
        True

    :type record: dict
    :rtype: bool
    """
    return "datumVymazu" not in record and bool(record.get("delete_date"))


def filter_active_records(records: list, allow_deleted: bool = False):
    """
    Filter out invalid records.

    Example:
    ========
        >>> data = [{"datumZapisu": "2020-01-01", "datumVymazu": "2022-01-01"},
        ...         {"datumZapisu": "2020-01-01"}]
        >>> filter_active_records(data)
        [{'datumZapisu': '2020-01-01'}]

    :param records: List of records
    :type records: list
    :param allow_deleted: Allow deleted records
    :type allow_deleted: bool
    :rtype: list
    """
    if allow_deleted:
        return records
    return [record for record in records if is_record_active(record)]
