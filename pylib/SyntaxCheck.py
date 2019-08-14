__author__ = 'bittremieux, walzer'
import json
import os
import urllib.request
from typing import Dict, List, Union

import jsonschema

class SyntacticCheck(object):
    def __init__(self, version: str=""):
        self.version = version  
        self.schema_url = 'https://raw.githubusercontent.com/HUPO-PSI/mzQC/' \
                     'master/schema/v{v}/mzqc_{v}.schema.json'.format(v=version)
        self.schema = None
        with urllib.request.urlopen(self.schema_url, timeout=2) as schema_in:
            self.schema = json.loads(schema_in.read().decode())

    def validate(self, mzqc_json):
        jsonschema.validate(mzqc_json, self.schema,
                            format_checker=jsonschema.FormatChecker())

