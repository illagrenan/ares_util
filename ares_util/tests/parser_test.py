#!/usr/bin/python
# coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library

standard_library.install_aliases()

from ..ares import get_czech_zip_code, guess_czech_street_from_full_text_address

from unittest import TestCase


class ZIPCodeTestCase(TestCase):
    def test_get_czech_zip_code(self):
        expected = "4200"
        actual = get_czech_zip_code(ares_data="", full_text_address="U obchodního rejstříku 15, Praha, PSČ 4200")
        self.assertEqual(expected, actual)

        expected = "1111"
        actual = get_czech_zip_code(ares_data="1111", full_text_address="U obchodního rejstříku 15, Praha, PSČ 2222")
        self.assertEqual(expected, actual)


class CzechStreetTestCase(TestCase):
    def test_get_czech_zip_code(self):
        full_text = "Praha, U Pythonisty 42/36, PSČ 4200"
        expected = "U Pythonisty 42/36"

        actual = guess_czech_street_from_full_text_address(full_text)

        self.assertEqual(expected, actual)
