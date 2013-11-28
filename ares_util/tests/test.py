#!/usr/bin/python
# coding=utf-8

from unittest2 import TestCase
import unittest2 as unittest
from ..ares import call_ares, validate_czech_company_id
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
    def test_invalid_values(self):
        with self.assertRaises(InvalidCompanyIDError):
            validate_czech_company_id(1234567)
            validate_czech_company_id(12345678)
            validate_czech_company_id("foo")

    def test_valid_values(self):
        self.assertTrue(validate_czech_company_id(68407700))
        self.assertTrue(validate_czech_company_id(27074358))
        self.assertTrue(validate_czech_company_id(27604977))
        self.assertTrue(validate_czech_company_id(26168685))


if __name__ == '__main__':
    unittest.main()