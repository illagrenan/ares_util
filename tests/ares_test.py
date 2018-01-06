# !/usr/bin/python
# coding=utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

import io
import os
from unittest import TestCase

import responses

from ares_util import ares
from ares_util.ares import call_ares, get_legal_form
from ares_util.exceptions import AresConnectionError, AresServerError
from ares_util.helpers import normalize_company_id_length
from ares_util.settings import ARES_API_URL


def _read_mock_response(filename):
    _this_dir = os.path.dirname(os.path.realpath(__file__))

    return io.open(os.path.join(_this_dir, "responses", filename), mode='r', encoding='utf-8').read()


class CallARESTestCase(TestCase):
    def test_invalid_values(self):
        invalid_values = [False, True, 42, -42, "foo"]

        for invalid_value in invalid_values:
            self.assertFalse(call_ares(invalid_value))

    @responses.activate
    def test_numerically_valid(self):
        company_id = 25596641
        responses.add(responses.GET, '{0}?ico={1}'.format(ARES_API_URL, company_id), match_querystring=True, body=_read_mock_response('{}.xml'.format(company_id)))

        self.assertFalse(call_ares(company_id=company_id))
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_encoding(self):
        company_id = 68407700
        responses.add(responses.GET, '{0}?ico={1}'.format(ARES_API_URL, company_id), match_querystring=True, body=_read_mock_response('{}.xml'.format(company_id)))

        ares_response = call_ares(company_id=company_id)

        self.assertEqual(ares_response['legal']['company_name'], "České vysoké učení technické v Praze")
        self.assertEqual(ares_response['address']['street'], "Zikova 1903/4")
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_special_case_for_issue9(self):
        company_id = 25834151
        responses.add(responses.GET, '{0}?ico={1}'.format(ARES_API_URL, company_id), match_querystring=True, body=_read_mock_response('{}.xml'.format(company_id)))

        ares_response = call_ares(company_id=company_id)

        self.assertEqual(ares_response['legal']['company_name'], "HELLA AUTOTECHNIK NOVA, s.r.o.")
        self.assertEqual(ares_response['address']['street'], "Družstevní 338/16")
        self.assertEqual(ares_response['address']['city'], "Mohelnice")
        self.assertEqual(ares_response['address']['zip_code'], "78985")
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_valid_values(self):
        other_valid_company_ids = ('25063677', '1603094', '01603094', '27074358')

        for one_id in other_valid_company_ids:
            responses.add(responses.GET, '{0}?ico={1}'.format(ARES_API_URL, one_id), match_querystring=True, body=_read_mock_response('{}.xml'.format(one_id)))

        try:
            for one_id in other_valid_company_ids:
                ares_data = call_ares(company_id=one_id)
                self.assertEqual(normalize_company_id_length(one_id), ares_data['legal']['company_id'])
        except KeyError as error:
            self.fail(error)

        self.assertEqual(len(other_valid_company_ids), len(responses.calls))

    def test_raises_ares_connection_exception(self):
        correct_url = ares.ARES_API_URL
        ares.ARES_API_URL = 'http://nonsenseurl.nonsence'
        self.assertRaises(AresConnectionError, call_ares, company_id='62739913')
        ares.ARES_API_URL = correct_url

    @responses.activate
    def test_raises_ares_server_error(self):
        company_id = 60159014
        responses.add(responses.GET, '{0}?ico={1}'.format(ARES_API_URL, company_id), match_querystring=True, body=_read_mock_response('server_fault.xml'))

        with self.assertRaises(AresServerError) as context:
            call_ares(company_id=company_id)

        self.assertEqual(context.exception.fault_code, u'Server.Service')
        self.assertEqual(context.exception.fault_message, u'obecná chyba serverové služby')


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
