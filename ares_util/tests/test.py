#!/usr/bin/python
# coding=utf-8
import warnings

from unittest2 import TestCase
import unittest2 as unittest
from ..ares import call_ares, validate_czech_company_id
from ..validators import czech_company_id_numeric_validator, czech_company_id_ares_api_validator
from ..exceptions import InvalidCompanyIDError


class CallARESTestCase(TestCase):
    def test_invalid_values(self):
        self.assertFalse(call_ares(False))
        self.assertFalse(call_ares(True))
        self.assertFalse(call_ares(42))
        self.assertFalse(call_ares(-42))
        self.assertFalse(call_ares("foo"))

    def test_valid_values(self):
        self.assertIsInstance(call_ares(27074358), dict)


class ValidateCzechBusinessIdTestCase(TestCase):
    invalid_values = [1234567, 12345678, "foo", "abcdefgh"]
    valid_values = [68407700, 27074358, 27604977, 26168685]

    def test_invalid_values(self):
        for invalid_value in self.invalid_values:
            with self.assertRaises(InvalidCompanyIDError):
                validate_czech_company_id(invalid_value)

            try:
                from django.core.exceptions import ValidationError

                with self.assertRaises(ValidationError):
                    czech_company_id_numeric_validator(invalid_value)

                with self.assertRaises(ValidationError):
                    czech_company_id_ares_api_validator(invalid_value)
            except ImportError:
                warnings.warn("Django is not installed")

    def test_valid_values(self):
        for valid_value in self.valid_values:
            self.assertTrue(validate_czech_company_id(valid_value))


if __name__ == '__main__':
    unittest.main()