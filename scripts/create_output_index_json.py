#!/usr/bin/env python3

import os
import sys
import json
import re


def change_file_ext(filename, extension):
    return os.path.splitext(filename)[0] + '.' + extension

def add_entire_directory_to_tab(tab, adoc_dir):
    dir_entries = os.listdir(adoc_dir)
    adoc_files = [f for f in dir_entries if os.path.isfile(os.path.join(adoc_dir, f)) and f.endswith(".adoc")]
    tab['subitems'] = []
    for this_file in adoc_files:
        newsubitem = {}
        newsubitem['title'] = this_file
        newsubitem['description'] = this_file
        newsubitem['subpath'] = this_file
        newsubitem['imagepath'] = os.path.join('/images', 'placeholder/placeholder_square.png')
        newsubitem['path'] = os.path.join(tab['path'], change_file_ext(newsubitem['subpath'], 'html'))
        tab['subitems'].append(newsubitem)

if __name__ == "__main__":
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    input_dir = sys.argv[3]
    with open(input_json) as json_fh:
        data = json.load(json_fh)
        found_default_tab = False
        for tab_index, tab in enumerate(data['tabs']):
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
            elif 'entire_directory' in tab:
                tab_dir = os.path.join(input_dir, tab['entire_directory'])
                if os.path.exists(tab_dir):
                    tab['path'] = '/{}/'.format(tab['entire_directory'])
                    add_entire_directory_to_tab(tab, tab_dir)
                else:
                    del data['tabs'][tab_index]
            else:
                raise Exception("Tab '{}' in '{}' has neither '{}' nor '{}'".format(tab['title'], input_json, 'path', 'entire_directory'))
        if not found_default_tab:
            print("WARNING: no default_tab set in {} so index page will look odd".format(input_json))

        with(open(output_json, 'w')) as output_fh:
            json.dump(data, output_fh, indent=4)
