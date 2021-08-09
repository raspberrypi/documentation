#!/usr/bin/env python3

import urllib.request
import sys
import re
import os
import shutil

outer_tag = 'esi-root'
offline_dir = 'offline_includes'

if len(sys.argv) != 3:
    raise Exception("Usage: {} <url> <outputfile>".format(sys.argv[0]))

url = sys.argv[1]
outputfile = sys.argv[2]

if os.getenv('OFFLINE_MODE', '0') == '1':
    print("Running in OFFLINE_MODE so copying files from {} instead".format(offline_dir))
    shutil.copyfile(os.path.join(offline_dir, os.path.basename(outputfile)), outputfile)
else:
    # Some servers reply with a 403 if the User-Agent isn't set ?!?!
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'grab-esi-fragment/0.1')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf8')
        m = re.search('<{0}>(.*)</{0}>'.format(outer_tag), html, re.DOTALL)
        if m:
            fragment = m.group(1)
            with open(outputfile, 'w') as output_fh:
                output_fh.write(fragment)
        else:
            raise Exception("Couldn't find '{}' tag in HTML returned for {}".format(outer_tag, url))
