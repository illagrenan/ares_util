# !/usr/bin/python
# coding=utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)


class InvalidCompanyIDError(Exception):
    pass


class AresNoResponseError(Exception):
    pass


class AresConnectionError(Exception):
    pass


class AresServerError(Exception):
    def __init__(self, fault_code, fault_message):
        super(AresServerError, self).__init__(fault_code, fault_message)
        self.fault_code = fault_code
        self.fault_message = fault_message

    def __repr__(self):
        return 'AresServerError, {}, {}'.format(self.fault_code, self.fault_message)
