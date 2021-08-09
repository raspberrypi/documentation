#!/usr/bin/env python3

import os.path
import sys
import json


def change_file_ext(filename, extension):
    return os.path.splitext(filename)[0] + '.' + extension


if __name__ == "__main__":
    input_json = sys.argv[1]
    output_json = sys.argv[2]

    with open(input_json) as json_fh:
        data = json.load(json_fh)
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
