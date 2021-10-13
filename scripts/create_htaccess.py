#!/usr/bin/env python3

import sys
import os
import csv
import urllib.request
import xml.etree.ElementTree as ET


DATASHEETS_BASE_URL = 'https://datasheets.raspberrypi.com'
DATASHEETS_BUCKET_URL = 'https://rptl-datasheets.s3.eu-west-1.amazonaws.com'
REDIRECT_SOURCE_PREFIX = '/documentation/'


if __name__ == "__main__":
    extra = sys.argv[1]
    redirects_dir = sys.argv[2]
    output_filename = sys.argv[3]

    any_datasheets_redirects = False
    redirects = dict()
    for filename in os.listdir(redirects_dir):
        if os.path.splitext(filename)[1] == '.csv':
            with open(os.path.join(redirects_dir, filename)) as csvfile:
                for row in csv.reader(csvfile):
                    if row:
                        old, new = row
                        if not old.startswith(REDIRECT_SOURCE_PREFIX):
                            raise Exception('Redirect {} doesn\'t start with {}'.format(REDIRECT_SOURCE_PREFIX))
                        if old in redirects:
                            raise Exception('Multiple redirects for source-URL {}'.format(old))
                        if new.startswith(DATASHEETS_BASE_URL):
                            any_datasheets_redirects = True
                        redirects[old] = new

    datasheets_filenames = set()
    if any_datasheets_redirects:
        # get list of "URLs" on the datasheets site
        req = urllib.request.Request(DATASHEETS_BUCKET_URL)
        with urllib.request.urlopen(req) as response:
            xml = response.read().decode('utf8')
            ns = {'S3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
            root = ET.fromstring(xml)
            for child in root.findall('S3:Contents', ns):
                if int(child.find('S3:Size', ns).text) > 0:
                    datasheets_filenames.add(child.find('S3:Key', ns).text)

    with open(output_filename, 'w') as out_fh:
        out_fh.write('<IfModule mod_alias.c>\n')
        for redir in sorted(redirects):
            link = redirects[redir]
            if link.startswith(DATASHEETS_BASE_URL):
                filepart = link[len(DATASHEETS_BASE_URL)+1:]
                if filepart not in datasheets_filenames:
                    raise Exception('{} seems to be an invalid URL'.format(link))
            out_fh.write('Redirect 301 {} {}\n'.format(redir, link))
        out_fh.write('</IfModule>\n')
        if os.path.isfile(extra):
            with open(extra) as extra_fh:
                out_fh.write(extra_fh.read())
                out_fh.write('\n')
