#!/usr/bin/python
# coding=utf-8

from unittest2 import TestCase
import unittest2 as unittest
from ..ares import call_ares


class CallARESTestCase(TestCase):
    def test_invalid_values(self):
        self.assertFalse(call_ares(False))
        self.assertFalse(call_ares(True))
        self.assertFalse(call_ares(42))
        self.assertFalse(call_ares(-42))
        self.assertFalse(call_ares("foo"))

    def test_valid_values(self):
        self.assertIsInstance(call_ares(27074358), dict)

        # IČ 25596641 je numericky platné, není však zaregistrované
        # Viz http://phpfashion.com/jak-overit-platne-ic-a-rodne-cislo
        self.assertFalse(call_ares(25596641), dict)


if __name__ == '__main__':
    unittest.main()