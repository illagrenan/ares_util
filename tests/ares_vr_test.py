# !/usr/bin/python
# coding=utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import pathlib
from unittest import TestCase

import requests
from requests.status_codes import codes

import responses

from ares_util.ares import call_ares_vr
from ares_util.exceptions import AresConnectionError, AresServerError
from ares_util.helpers import normalize_company_id_length
from ares_util.settings import ARES_VR_API_URL


def _json_response(company_id):
    this_dir = pathlib.Path(os.path.realpath(__file__)).parent
    return (this_dir / "responses" / "vr" / f"{company_id}.json").read_text()


class CallARESVRTestCase(TestCase):
    def test_invalid_values(self):
        invalid_values = [False, True, 42, -42, "foo", 25596640]

        for invalid_value in invalid_values:
            self.assertFalse(call_ares_vr(invalid_value))

    @responses.activate
    def test_not_found(self):
        company_id = "01603094"
        responses.get(f'{ARES_VR_API_URL}{company_id}', body=_json_response(company_id), status=codes.not_found)

        self.assertFalse(call_ares_vr(company_id=company_id))
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_valid_values(self):
        company_ids = ('25063677', '25834151', '27074358')

        try:
            for company_id in company_ids:
                responses.get(f'{ARES_VR_API_URL}{company_id}', body=_json_response(company_id))

                ares_data = call_ares_vr(company_id=company_id)
                self.assertEqual(normalize_company_id_length(company_id), ares_data['company_id'])
        except KeyError as error:
            self.fail(error)

        self.assertEqual(len(company_ids), len(responses.calls))

    @responses.activate
    def test_raises_ares_connection_exception(self):
        company_id = '62739913'
        responses.get(f'{ARES_VR_API_URL}{company_id}', body=requests.ConnectionError("Connection refused"))

        with self.assertRaises(AresConnectionError):
            call_ares_vr(company_id=company_id)

    @responses.activate
    def test_raises_ares_server_error(self):
        company_id = '60159014'
        responses.get(
            f'{ARES_VR_API_URL}{company_id}',
            body=_json_response('server_error'),
            status=codes.internal_server_error
        )

        with self.assertRaises(AresServerError) as context:
            call_ares_vr(company_id=company_id)

        self.assertEqual(context.exception.fault_code, 'OBECNA_CHYBA')
        self.assertIsNotNone(context.exception.fault_message)
