# !/usr/bin/python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
from unittest import TestCase

from ..ares import get_czech_zip_code, guess_czech_street_from_full_text_address, build_city


class ZIPCodeTestCase(TestCase):
    def test_get_czech_zip_code(self):
        expected = "4200"
        actual = get_czech_zip_code(ares_data="", full_text_address="U obchodního rejstříku 15, Praha, PSČ 4200")
        self.assertEqual(expected, actual)

        expected = "1111"
        actual = get_czech_zip_code(ares_data="1111", full_text_address="U obchodního rejstříku 15, Praha, PSČ 2222")
        self.assertEqual(expected, actual)

    @unittest.skip("This will be fixed in the next verion")
    def test_get_czech_zip_code_1(self):
        expected = "27704"
        actual = get_czech_zip_code(ares_data="", full_text_address="Daminěves 35, 277 04 Cítov")

        self.assertEqual(expected, actual)


class CzechStreetTestCase(TestCase):
    def test_get_street(self):
        full_text = "Praha, U Pythonisty 42/36, PSČ 4200"
        expected = "U Pythonisty 42/36"

        actual = guess_czech_street_from_full_text_address(full_text)

        self.assertEqual(expected, actual)

    @unittest.skip("This will be fixed in the next verion")
    def test_get_street_reversed(self):
        full_text = "Daminěves 35, 277 04 Cítov"
        expected = "Daminěves 35"

        actual = guess_czech_street_from_full_text_address(full_text)

        self.assertEqual(expected, actual)


class CityTestCase(TestCase):
    @unittest.skip("This will be fixed in the next verion")
    def test_get_czech_zip_code(self):
        full_text = "Daminěves 35, 277 04 Cítov"
        expected = "Cítov"

        actual = build_city(city=None, address=full_text)

        self.assertEqual(expected, actual)
