# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import json

sys.path.insert(1, os.path.normpath('../..'))


def main():
    from ares_util.ares import call_ares

    with open('output.json', 'w') as f:
        ctu_company_id = "68407700"
        data = call_ares(ctu_company_id)
        f.write(json.dumps(data, indent=5))


if __name__ == "__main__":
    main()

    sys.exit(1)
