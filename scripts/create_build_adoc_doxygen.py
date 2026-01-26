#!/usr/bin/env python3

import sys
import os
import json
import re
import yaml


def check_no_markdown(filename):
    with open(filename) as fh:
        asciidoc = fh.read()
        if re.search(r'```\n.*?\n```', asciidoc):
            raise Exception("{} uses triple-backticks for markup - please use four-hyphens instead".format(filename))
        # strip out code blocks
        asciidoc = re.sub(r'----\n.*?\n----', '', asciidoc, flags=re.DOTALL)
        # strip out pass-through blocks
        asciidoc = re.sub(r'\+\+\+\+\n.*?\n\+\+\+\+', '', asciidoc, flags=re.DOTALL)
        if re.search(r'(?:^|\n)#+', asciidoc):
            raise Exception("{} contains a Markdown-style header (i.e. '#' rather than '=')".format(filename))
        if re.search(r'(\[.+?\]\(.+?\))', asciidoc):
            raise Exception("{} contains a Markdown-style link (i.e. '[title](url)' rather than 'url[title]')".format(filename))


if __name__ == "__main__":
    index_json = sys.argv[1]
    config_yaml = sys.argv[2]
    page_preamble = sys.argv[3]
    src_adoc = sys.argv[4]
    picosdk_json = sys.argv[5]
    includes_dir = sys.argv[6]
    build_adoc = sys.argv[7]

    output_subdir = os.path.basename(os.path.dirname(build_adoc))
    adoc_filename = os.path.basename(build_adoc)

    check_no_markdown(src_adoc)

    with open(picosdk_json) as json_fh:
        picosdk_data = json.load(json_fh)

    index_title = None
    with open(index_json) as json_fh:
        data = json.load(json_fh)
        for tab in data['tabs']:
            if 'from_json' in tab and 'directory' in tab and tab['directory'] == output_subdir:
                filebase = os.path.splitext(adoc_filename)[0]
                index_title = filebase
                picosdk_filename = filebase+".html"
                for item in picosdk_data:
                    if re.sub("^group__", "", item["html"]) == picosdk_filename:
                        index_title = item['name']
                        break
    if index_title is None:
        raise Exception("Couldn't find title for {} in {}".format(os.path.join(output_subdir, adoc_filename), index_json))

    with open(config_yaml) as config_fh:
        site_config = yaml.safe_load(config_fh)

    with open(page_preamble) as preamble_fh:
        preamble_template = preamble_fh.read()
        template_vars = {
            'output_subdir': output_subdir,
            'includes_dir': includes_dir,
            'site_title': site_config['title'],
            'page_title': index_title,
        }
        preamble_text = re.sub(r'{{\s*(\w+)\s*}}', lambda m: template_vars[m.group(1)], preamble_template)

    new_contents = preamble_text + "\n"
    with open(src_adoc) as in_fh:
        seen_header = False
        for line in in_fh.readlines():
            if re.match('^=+ ', line) is not None:
                if not seen_header:
                    seen_header = True
            else:
                m = re.match(r'^(include::)(.+)(\[\]\n?)$', line)
                if m:
                    line = m.group(1) + os.path.join('{includedir}/{parentdir}', m.group(2)) + m.group(3)
            new_contents += line

    with open(build_adoc, 'w') as out_fh:
        out_fh.write(new_contents)
