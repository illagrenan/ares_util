# !/usr/bin/python
# coding=utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

from urllib.parse import urljoin

COMPANY_ID_LENGTH = 8
ARES_BASE_URL = 'https://ares.gov.cz/'
ARES_API_URL = urljoin(ARES_BASE_URL, f'ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/')
