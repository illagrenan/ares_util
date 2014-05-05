#!/usr/bin/python
# coding=utf-8

from unittest2 import TestCase
from ..ares import call_ares


class CallARESTestCase(TestCase):
    def test_invalid_values(self):
        self.assertFalse(call_ares(False))
        self.assertFalse(call_ares(True))
        self.assertFalse(call_ares(42))
        self.assertFalse(call_ares(-42))
        self.assertFalse(call_ares("foo"))

    def test_valid_values(self):
        self.assertIsInstance(call_ares(company_id=27074358), dict)

        # IČ 25596641 je numericky platné, není však zaregistrované
        # Viz http://phpfashion.com/jak-overit-platne-ic-a-rodne-cislo
        self.assertFalse(call_ares(company_id=25596641), dict)

        actual = call_ares(company_id=68407700)['address']['street']
        # ČVUT v Praze
        expected = "Zikova 1903/2"
        self.assertEqual(actual, expected)

        try:
            for id in (62739913, 25063677):
                call_ares(company_id=id)
        except KeyError as error:
            self.fail(error)
