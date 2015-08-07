# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from flask import Flask
import flask

from ares_util.ares import call_ares

app = Flask(__name__)


@app.route('/<string:post_id>')
def ares_json_response(post_id):
    ares_response = call_ares(company_id=post_id)

    return flask.jsonify(**ares_response)


if __name__ == '__main__':
    # Attention:
    # ==========
    # Even though the interactive debugger does not work in forking environments (which makes it
    # nearly impossible to use on production servers), it still allows the execution of arbitrary
    # code. This makes it a major security risk and therefore it must never be used on production machines.

    app.debug = True

    # ==========

    app.run()
