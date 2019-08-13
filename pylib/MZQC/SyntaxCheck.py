__author__ = 'bittremieux, walzer'
import json
import os
import urllib.request
from typing import Dict, List, Union

import jsonschema
from jsonschema.exceptions import ValidationError

class SyntacticCheck(object):
    def __init__(self, version: str=""):
        self.version = version  
        # self.schema_url = 'https://raw.githubusercontent.com/HUPO-PSI/mzQC/' \
        #              'mzqc-pylib/schema/v{v}/mzqc_{v}.schema.json'.format(v=version)
        with open('tests/schema.json', 'r') as s:
            self.schema = json.loads(s.read())
        # self.schema_url = 'https://raw.githubusercontent.com/HUPO-PSI/mzQC/' \
                    #  'master/schema/v{v}/mzqc_{v}.schema.json'.format(v=version)
        # self.schema_url = "https://raw.githubusercontent.com/HUPO-PSI/mzQC/master/schema/v0_0_11/mzqc_0_0_11.schema.json"
        # self.schema = None
        # with urllib.request.urlopen(self.schema_url, timeout=2) as schema_in:
        #     self.schema = json.loads(schema_in.read().decode())

    def validate(self, mzqc_str: str):
        try:
            mzqc_json = json.loads(mzqc_str)
        except:
            raise ValidationError("Given mzqc seems not to be a string representation of a json type.")
        return jsonschema.validate(mzqc_json, self.schema, format_checker=jsonschema.FormatChecker())
