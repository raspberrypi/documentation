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

needed_internal_links = dict()
def read_file_with_includes(filepath, output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(filepath)
    content = ''
    with open(filepath) as adoc_fh:
        if filepath not in needed_internal_links:
            needed_internal_links[filepath] = []
        parent_dir = os.path.dirname(filepath)
        for line in adoc_fh.readlines():
            for m in re.finditer(r'xref:(.+?)(?:#(.+?))?\[.*?\]', line):
                link = m.group(1)
                anchor = m.group(2)
                if not link.endswith('.adoc'):
                    raise Exception("{} links to non-adoc file {}".format(filepath, link))
                link_path = os.path.normpath(os.path.join(output_dir, link))
                link_relpath = os.path.relpath(link_path, adoc_dir)
                linkinfo = {'url': link_relpath}
                if anchor:
                    linkinfo['anchor'] = anchor
                needed_internal_links[filepath].append(linkinfo)
            m = re.match(r'^include::(.*)\[\]\s*$', line)
            if m:
                content += read_file_with_includes(os.path.join(parent_dir, m.group(1)), output_dir)
            else:
                content += line
    return content

min_level = 2 # this has to be 2
max_level = 3 # this can be 2 or 3

if __name__ == "__main__":
    index_json = sys.argv[1]
    adoc_dir = sys.argv[2]
    output_json = sys.argv[3]

    with open(index_json) as json_fh:
        data = json.load(json_fh)
        output_data = []
        available_anchors = dict()
        for tab in data['tabs']:
            nav = []
            if 'path' in tab:
                for subitem in tab['subitems']:
                    if 'subpath' in subitem:
                        fullpath = os.path.join(tab['path'], subitem['subpath'])
                        if fullpath in available_anchors:
                            raise Exception("{} occurs twice in {}".format(fullpath, index_json))
                        available_anchors[fullpath] = set()
                        nav.append({
                            'path': os.path.join('/', change_file_ext(fullpath, 'html')),
                            'title': subitem['title'],
                            'sections': [],
                        })
                        level = min_level
                        adjusted_path = re.sub("^/", "", fullpath)
                        top_level_file = os.path.join(adoc_dir, adjusted_path)
                        adoc_content = read_file_with_includes(top_level_file)
                        last_line_was_discrete = False
                        header_id = None
                        for line in adoc_content.split('\n'):
                            m = re.match(r'^\[\[(.*)\]\]\s*$', line)
                            if m:
                                header_id = m.group(1)
                            else:
                                m = re.match(r'^\[(.*)\]\s*$', line)
                                if m:
                                    attrs = m.group(1).split(',')
                                    last_line_was_discrete = 'discrete' in attrs
                                    header_id = None
                                else:
                                    m = re.match(r'^(=+)\s+(.+?)\s*$', line)
                                    if m:
                                        newlevel = len(m.group(1))
                                        # Need to compute anchors for *every* header (updates file_headings)
                                        heading = strip_adoc(m.group(2))
                                        anchor = heading_to_anchor(top_level_file, heading, header_id)
                                        if anchor in available_anchors[fullpath]:
                                            raise Exception("Anchor {} appears twice in {}".format(anchor, fullpath))
                                        available_anchors[fullpath].add(anchor)
                                        if min_level <= newlevel <= max_level and not last_line_was_discrete:
                                            entry = {'heading': heading, 'anchor': anchor}
                                            if newlevel > level:
                                                nav[-1]['sections'][-1]['subsections'] = []
                                            level = newlevel
                                            if level == 2:
                                                nav[-1]['sections'].append(entry)
                                            elif level == 3:
                                                nav[-1]['sections'][-1]['subsections'].append(entry)
                                    last_line_was_discrete = False
                                    header_id = None
            elif 'from_json' in tab:
                tab_dir = os.path.join(adoc_dir, tab['directory'])
                if os.path.exists(tab_dir):
                    # TODO: Need to do something here to create the appropriate nav entries for tab['from_json']
                    pass
            else:
                raise Exception("Tab '{}' in '{}' has neither '{}' nor '{}'".format(tab['title'], index_json, 'path', 'from_json'))

            output_data.append({'title': tab['title'], 'path': '{}'.format(tab.get('path', tab.get('from_json'))), 'toc': nav})
        for filepath in sorted(needed_internal_links):
            for linkinfo in needed_internal_links[filepath]:
                if not linkinfo['url'].startswith('pico-sdk/'): # these pages aren't created by a non-doxygen build
                    adjusted_url = "/" + linkinfo['url']
                    if adjusted_url not in available_anchors:
                        raise Exception("{} has an internal-link to {} but that destination doesn't exist".format(filepath, adjusted_url))
                    if 'anchor' in linkinfo:
                        if linkinfo['anchor'] not in available_anchors[adjusted_url]:
                            raise Exception("{} has an internal-link to {}#{} but that anchor doesn't exist. Available anchors: {}".format(filepath, adjusted_url, linkinfo['anchor'], ', '.join(sorted(available_anchors[adjusted_url]))))

        with open(output_json, 'w') as out_fh:
            json.dump(output_data, out_fh, indent=4)
