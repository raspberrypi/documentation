#!/usr/bin/env python3

import os
import sys
import json
import re


def change_file_ext(filename, extension):
    return os.path.splitext(filename)[0] + '.' + extension

def get_global_subitems():
    scripts_dir = os.path.dirname(__file__)
    json_path = os.path.join(scripts_dir, "global_boxes.json")
    with open(json_path) as json_fh:
        items = json.load(json_fh)
    return items

def build_tab_from_json(tab, adoc_dir, img_dir):
    json_path = os.path.join(adoc_dir, tab['from_json'])
    tab_key = tab['directory']
    box_images_dir = os.path.join(img_dir, "full-sized")
    available_images = os.listdir(box_images_dir)
    available_images = sorted([f for f in available_images if re.search(tab_key+"_", f) is not None])
    with open(json_path) as json_fh:
        tab_data = json.load(json_fh)
        tab['subitems'] = []
        counter = 0
        for item in tab_data:
            newsubitem = {}
            newsubitem['title'] = tab_data[item]['name']
            newsubitem['description'] = tab_data[item]['description']
            newsubitem['subpath'] = item + ".adoc"
            if len(available_images) > counter:
                newsubitem['imagepath'] = os.path.join('/images', 'full-sized', available_images[counter])
            else:
                newsubitem['imagepath'] = os.path.join('/images', 'placeholder/placeholder_square.png')
            newsubitem['path'] = os.path.join(tab['path'], change_file_ext(newsubitem['subpath'], 'html'))
            tab['subitems'].append(newsubitem)
            counter += 1

if __name__ == "__main__":
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    input_dir = sys.argv[3]
    images_dir = sys.argv[4]
    global_subitems = get_global_subitems()
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
            elif 'from_json' in tab:
                tab_dir = os.path.join(input_dir, tab['directory'])
                if os.path.exists(tab_dir):
                    tab['path'] = '/{}/'.format(tab['directory'])
                    build_tab_from_json(tab, tab_dir, images_dir)
                else:
                    del data['tabs'][tab_index]
            else:
                raise Exception("Tab '{}' in '{}' has neither '{}' nor '{}'".format(tab['title'], input_json, 'path', 'from_json'))
            # add the global boxes
            if 'subitems' in tab:
                for item in global_subitems:
                    tab['subitems'].append(item)
            else:
                print("WARNING: no subitems set in {}".format(tab['title']))
        if not found_default_tab:
            print("WARNING: no default_tab set in {} so index page will look odd".format(input_json))

        with(open(output_json, 'w')) as output_fh:
            json.dump(data, output_fh, indent=4)
