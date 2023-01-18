#!/usr/bin/env python3

import os
import sys
import json
import re


def change_file_ext(filename, extension):
    return os.path.splitext(filename)[0] + '.' + extension

def add_picosdk_entries(data, adoc_dir):
    adoc_files = os.listdir(adoc_dir)
    adoc_files = [f for f in adoc_files if re.search(".adoc", f) is not None]
    pidosdk_item = {}
    for tab in data['tabs']:
        if 'path' in tab and tab['path'] == "pico-sdk":
            pidosdk_item = tab
    if 'subitems' not in tab:
        tab['subitems'] = []
    for this_file in adoc_files:
        newsubitem = {}
        newsubitem['title'] = this_file
        newsubitem['description'] = this_file
        newsubitem['subpath'] = this_file
        tab['subitems'].append(newsubitem)
    return data

if __name__ == "__main__":
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    adoc_dir = sys.argv[3]
    with open(input_json) as json_fh:
        data = json.load(json_fh)
        data = add_picosdk_entries(data, adoc_dir)
        found_default_tab = False
        for tab in data['tabs']:
            if 'default_tab' in tab and tab['default_tab'] == "yes":
                if found_default_tab:
                    raise Exception("More than one default_tab set in {}".format(input_json))
                found_default_tab = True
            if 'path' in tab:
                tab['path'] = '/{}/'.format(tab['path'])
                for subitem in tab['subitems']:
                    if 'subpath' in subitem:
                        subitem['path'] = os.path.join(tab['path'], change_file_ext(subitem['subpath'], 'html'))
                    if 'image' in subitem:
                        subitem['imagepath'] = os.path.join('/images', subitem['image'])
        if not found_default_tab:
            print("WARNING: no default_tab set in {} so index page will look odd".format(input_json))

        with(open(output_json, 'w')) as output_fh:
            json.dump(data, output_fh, indent=4)
