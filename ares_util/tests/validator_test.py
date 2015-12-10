#!/usr/bin/python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from unittest2 import TestCase
from django.core.exceptions import ValidationError

from ..ares import validate_czech_company_id
from ..exceptions import InvalidCompanyIDError
from ..validators import czech_company_id_numeric_validator, czech_company_id_ares_api_validator


class ValidateCzechBusinessIdTestCase(TestCase):
    invalid_values = [1234567, 12345678, "foo", "abcdefgh"]
    valid_values = [68407700, 27074358, 27604977, 26168685, 25596641, 62739913, "1603094", "01603094"]

    def test_invalid_values(self):
        for invalid_value in self.invalid_values:
            with self.assertRaises(InvalidCompanyIDError):
                validate_czech_company_id(invalid_value)

            with self.assertRaises(ValidationError):
                czech_company_id_numeric_validator(invalid_value)

            with self.assertRaises(ValidationError):
                czech_company_id_ares_api_validator(invalid_value)

    def test_valid_values(self):
        for valid_value in self.valid_values:
            self.assertTrue(validate_czech_company_id(valid_value))
