# !/usr/bin/python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class InvalidCompanyIDError(Exception):
    pass


class AresNoResponseError(Exception):
    pass


class AresConnectionError(Exception):
    pass
