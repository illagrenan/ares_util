#!/usr/bin/python
# coding=utf-8

from __future__ import unicode_literals

from unittest import TestCase

from ..ares import call_ares, get_legal_form
from .. import ares
from ..helpers import normalize_company_id_length
from ..exceptions import AresConnectionError


class CallARESTestCase(TestCase):
    def test_invalid_values(self):
        invalid_values = [False, True, 42, -42, "foo"]

        for invalid_value in invalid_values:
            self.assertFalse(call_ares(invalid_value))

    def test_numerically_valid(self):
        # IČ 25596641 je numericky platné, není však zaregistrované
        # Viz http://phpfashion.com/jak-overit-platne-ic-a-rodne-cislo
        self.assertFalse(call_ares(company_id=25596641), dict)

    def test_encoding(self):
        ares_response = call_ares(company_id=68407700)

        self.assertEqual(ares_response['legal']['company_name'], "České vysoké učení technické v Praze")
        self.assertEqual(ares_response['address']['street'], "Zikova 1903/4")

    def test_special_case_for_issue9(self):
        ares_response = call_ares(company_id=25834151)

        self.assertEqual(ares_response['legal']['company_name'], "HELLA AUTOTECHNIK NOVA, s.r.o.")
        self.assertEqual(ares_response['address']['street'], "Družstevní 338/16")
        self.assertEqual(ares_response['address']['city'], "Mohelnice")
        self.assertEqual(ares_response['address']['zip_code'], "78985")

    def test_valid_values(self):
        other_valid_company_ids = ('62739913', '25063677', '1603094', '01603094', '27074358')

        try:
            for one_id in other_valid_company_ids:
                ares_data = call_ares(company_id=one_id)
                self.assertEqual(normalize_company_id_length(one_id), ares_data['legal']['company_id'])
        except KeyError as error:
            self.fail(error)

    def test_raises_ares_connection_exception(self):
        correct_url = ares.ARES_API_URL
        ares.ARES_API_URL = 'http://nonsenseurl.nonsence'
        self.assertRaises(AresConnectionError, call_ares, company_id='62739913')
        ares.ARES_API_URL = correct_url


class LegalFormTest(TestCase):
    def test_get_legal_form_if_present(self):
        valid_legal_form = "121"

        valid_partial_ares_api_response = {
            'D:KPF': valid_legal_form
        }

        actual_legal_form = get_legal_form(valid_partial_ares_api_response)
        self.assertEqual(valid_legal_form, actual_legal_form)

    def test_get_none_if_legal_form_not_present(self):
        empty_ares_api_call_response = {}

        self.assertIsNone(get_legal_form(empty_ares_api_call_response))
