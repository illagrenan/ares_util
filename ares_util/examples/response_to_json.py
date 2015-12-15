# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import json
import os
import sys

sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))


def main():
    from ares_util.ares import call_ares

    with open('output.json', 'w') as output_file:
        ctu_company_id = "68407700"
        data = call_ares(ctu_company_id)
        output_file.write(json.dumps(data, indent=5))


if __name__ == "__main__":
    main()

    sys.exit(1)
