#!/usr/bin/env python3

import sys
import os
import csv
import urllib.request
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    extra = sys.argv[1]
    output_filename = sys.argv[2]

    with open(output_filename, 'w') as out_fh:
        if os.path.isfile(extra):
            with open(extra) as extra_fh:
                out_fh.write(extra_fh.read())
                out_fh.write('\n')
