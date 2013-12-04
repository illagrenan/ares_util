#!/usr/bin/python
# coding=utf-8

from unittest2 import TestCase
import unittest2 as unittest
from ..ares import build_czech_address


class AddressTestCase(TestCase):
    def test_czech_address_build(self):
        expected = "1520/11"
        actual = build_czech_address(house_number=1520, orientation_number=11)
        self.assertEqual(expected, actual)

        expected = "16"
        actual = build_czech_address(house_number=16, orientation_number=None)
        self.assertEqual(expected, actual)

        expected = "32"
        actual = build_czech_address(house_number=32, orientation_number="")
        self.assertEqual(expected, actual)

        expected = "64"
        actual = build_czech_address(house_number=64, orientation_number=False)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()