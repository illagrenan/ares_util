# !/usr/bin/python
# coding=utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

from unittest import TestCase

from ares_util.ares import build_czech_street


class AddressTestCase(TestCase):
    def test_czech_address_build(self):
        expected = "Štichova 654/54"
        actual = build_czech_street(street_name="Štichova", city_name="Praha", neighborhood="Praha 4", house_number=654,
                                    orientation_number=54, full_text_address='Štichova 654/54, Praha 4')
        self.assertEqual(expected, actual)

        expected = "Vysoká Pec 216"
        actual = build_czech_street(street_name=None, city_name="Bohutín", neighborhood="Vysoká Pec", house_number=216,
                                    orientation_number=False, full_text_address="Vysoká Pec 216, Bohutín")
        self.assertEqual(expected, actual)

        expected = "Bohutín 310"
        actual = build_czech_street(street_name="", city_name="Bohutín", neighborhood="", house_number=310,
                                    orientation_number=False, full_text_address="Bohutín 310")
        expected = "Vaníčkova 11"
        actual = build_czech_street(street_name="", city_name="", neighborhood="", house_number=None,
                                    orientation_number=False, full_text_address="Ústí nad Labem-město, Vaníčkova 11")
        self.assertEqual(expected, actual)

    def test_special_case_for_issue9(self):
        expected = "Družstevní 338/16"

        actual = build_czech_street(street_name=None, city_name=None, neighborhood=None, house_number=None,
                                    orientation_number=None,
                                    full_text_address="Mohelnice, Družstevní 338/16, PSČ 78985")

        self.assertEqual(expected, actual)
