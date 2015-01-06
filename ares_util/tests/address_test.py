#!/usr/bin/python
# coding=utf-8

from __future__ import unicode_literals

from unittest2 import TestCase

from ..ares import build_czech_street


class AddressTestCase(TestCase):
    def test_czech_address_build(self):
        expected = "Štichova 654/54"
        actual = build_czech_street(street_name="Štichova", city_name="Praha", neighborhood="Praha 4", house_number=654,
                                    orientation_number=54, address='Štichova 654/54, Praha 4')
        self.assertEqual(expected, actual)

        expected = "Vysoká Pec 216"
        actual = build_czech_street(street_name=None, city_name="Bohutín", neighborhood="Vysoká Pec", house_number=216,
                                    orientation_number=False, address="Vysoká Pec 216, Bohutín")
        self.assertEqual(expected, actual)

        expected = "Bohutín 310"
        actual = build_czech_street(street_name="", city_name="Bohutín", neighborhood="", house_number=310,
                                    orientation_number=False, address="Bohutín 310")
        expected = "Vaníčkova 11"
        actual = build_czech_street(street_name="", city_name="", neighborhood="", house_number=None,
                                    orientation_number=False, address="Ústí nad Labem-město, Vaníčkova 11")
        self.assertEqual(expected, actual)
