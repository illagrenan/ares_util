# !/usr/bin/python
# coding=utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

import json

import flask
from flask import Flask

from ares_util.ares import call_ares

app = Flask(__name__)


@app.route('/<string:post_id>', methods=['GET', 'OPTIONS'])
def ares_json_response(post_id):
    ares_response = call_ares(company_id=post_id)
    json_data = json.dumps(ares_response)

    return flask.Response(json_data, status=200, mimetype='application/json')


if __name__ == '__main__':
    # Attention:
    # ==========
    # Even though the interactive debugger does not work in forking environments (which makes it
    # nearly impossible to use on production servers), it still allows the execution of arbitrary
    # code. This makes it a major security risk and therefore it must never be used on production machines.

    app.debug = True

    # ==========

    app.run()
