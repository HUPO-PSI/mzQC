#!/usr/bin/env python
__author__ = 'walzer'
import sys
import os
from datetime import datetime
import logging
import argparse
import pyopenms as oms
import sys
import json
from os.path import isfile, isdir, join, basename, splitext
import argparse
from datetime import datetime
import logging
import QCMLFile

VERSION = "0.4"


def __main__():
    parser = argparse.ArgumentParser(version=VERSION)
    parser.add_argument('-in', dest="inf", help='<Required> full path to the input file', required=True)
    parser.add_argument('-out', dest="out", help="<Required> full path to the output file", required=True)

    options = parser.parse_args()
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    filter = ["ABRACADABRA"]
    pros = list()
    peps = list()
    f = oms.IdXMLFile()
    f.load(options.inf, pros, peps)

    for pep in peps:
        hits = pep.getHits()
        nhits = list()
        for h in hits:
            if h.getSequence().toUnmodifiedString() not in filter:
                h.setMetaValue('qcWHAAA', 123)
                h.setMetaValue("MS:123", "asd")
                nhits.append(h)
            else:
                nhits.append(h)
        pep.setHits(nhits)

    f.store(options.out, pros, peps)


if __name__ == '__main__':
    __main__()
