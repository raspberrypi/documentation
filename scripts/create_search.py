#!/usr/bin/env python3

import sys
import os
import json
import re


def change_file_ext(filename, extension):
    return os.path.splitext(filename)[0] + '.' + extension

def strip_adoc(heading):
    return re.sub(r'\b(_|\*)(.+?)\1\b', r'\2', heading.replace('`', ''))

file_headings = dict()
def heading_to_anchor(filepath, heading, anchor):
    if anchor is None:
        # The replace(' -- ', '') is needed because AsciiDoc transforms ' -- ' to '&#8201;&#8212;&#8201;' (narrow-space, em-dash, narrow-space) which then collapses down to '' when calculating the anchor
        anchor = re.sub(r'\-+', '-', re.sub(r'[^-\w]', '', heading.lower().replace(' -- ', '').replace(' ', '-').replace('.', '-')))
    if filepath not in file_headings:
        file_headings[filepath] = set()
    proposed_anchor = anchor
    num = 1 # this isn't a logic bug, the first duplicate anchor gets suffixed with "-2"
    while proposed_anchor in file_headings[filepath]:
        num += 1
        proposed_anchor = '{}-{}'.format(anchor, num)
    file_headings[filepath].add(proposed_anchor)
    return proposed_anchor

def read_file_with_includes(filepath):
    content = ''
    with open(filepath) as adoc_fh:
        parent_dir = os.path.dirname(filepath)
        for line in adoc_fh.readlines():
            m = re.match(r'^include::(.*)\[\]\s*$', line)
            if m:
                content += read_file_with_includes(os.path.join(parent_dir, m.group(1)))
            else:
                content += line
    return content

min_level = 2 # this has to be 2
max_level = 4 # this can be 2, 3 or 4

if __name__ == "__main__":
    index_json = sys.argv[1]
    adoc_dir = sys.argv[2]
    output_json = sys.argv[3]

    with open(index_json) as json_fh:
        data = json.load(json_fh)
        output_data = []
        for tab in data['tabs']:
            nav = []
            for subitem in tab['subitems']:
                if 'subpath' in subitem:
                    nav.append({
                        'path': os.path.join('/', tab['path'], change_file_ext(subitem['subpath'], 'html')),
                        'title': subitem['title'],
                        'sections': [],
                    })
                    level = min_level
                    top_level_file = os.path.join(adoc_dir, tab['path'], subitem['subpath'])
                    adoc_content = read_file_with_includes(top_level_file)
                    header_id = None
                    for line in adoc_content.split('\n'):
                        m = re.match(r'^\[\[(.*)\]\]\s*$', line)
                        if m:
                            header_id = m.group(1)
                        else:
                            m = re.match(r'^(=+)\s+(.+?)\s*$', line)
                            if m:
                                # Need to compute anchors for *every* header (updates file_headings)
                                newlevel = len(m.group(1))
                                heading = strip_adoc(m.group(2))
                                anchor = heading_to_anchor(top_level_file, heading, header_id)
                                if min_level <= newlevel <= max_level:
                                    # Treat levels 3 and 4 identically
                                    if newlevel > 3:
                                        newlevel = 3
                                    entry = {'heading': heading, 'anchor': anchor}
                                    if newlevel > level:
                                        nav[-1]['sections'][-1]['subsections'] = []
                                    level = newlevel
                                    if level == 2:
                                        nav[-1]['sections'].append(entry)
                                    elif level == 3:
                                        nav[-1]['sections'][-1]['subsections'].append(entry)
                            header_id = None
            output_data.append({'title': tab['title'], 'path': '/{}/'.format(tab['path']), 'toc': nav})
        with open(output_json, 'w') as out_fh:
            json.dump(output_data, out_fh, indent=4)
