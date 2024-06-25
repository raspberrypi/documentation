#!/usr/bin/env python3

import sys
import os
import re
import yaml
import hashlib


def check_no_markdown(filename):
    with open(filename) as fh:
        asciidoc = fh.read()
        if re.search('```\n.*?\n```', asciidoc):
            raise Exception("{} uses triple-backticks for markup - please use four-hyphens instead".format(filename))
        # strip out code blocks
        asciidoc = re.sub(r'----\n.*?\n----', '', asciidoc, flags=re.DOTALL)
        # strip out pass-through blocks
        asciidoc = re.sub(r'\+\+\+\+\n.*?\n\+\+\+\+', '', asciidoc, flags=re.DOTALL)
        if re.search('(?:^|\n)#+', asciidoc):
            raise Exception("{} contains a Markdown-style header (i.e. '#' rather than '=')".format(filename))
        if re.search(r'(\[.+?\]\(.+?\))', asciidoc):
            raise Exception("{} contains a Markdown-style link (i.e. '[title](url)' rather than 'url[title]')".format(filename))


if __name__ == "__main__":
    config_yaml = sys.argv[1]
    github_edit = sys.argv[2]
    src_adoc = sys.argv[3]
    build_adoc = sys.argv[4]

    check_no_markdown(src_adoc)

    with open(config_yaml) as config_fh:
        site_config = yaml.safe_load(config_fh)

    with open(github_edit) as edit_fh:
        edit_template = edit_fh.read()
        template_vars = {
            'github_edit_link': os.path.join(site_config['githuburl'], 'blob', site_config['githubbranch_edit'], src_adoc)
        }
        edit_text = re.sub(r'{{\s*(\w+)\s*}}', lambda m: template_vars[m.group(1)], edit_template)

    with open(src_adoc) as in_fh:
        new_contents = ''
        seen_header = False
        for line in in_fh.readlines():
            if re.match(r'^=+ ', line) is not None:
                if not seen_header:
                    seen_header = True
                    if github_edit is not None:
                        line += edit_text + "\n\n"
            else:
                # find all image references, append md5 hash at end to bust the cache if we change the image
                m = re.match(r'^(image::)(.+)(\[(.+)]\n?)$', line)
                if m:
                    directory = os.path.dirname(os.path.abspath(src_adoc))
                    image_hash = hashlib.md5(open(os.path.join(directory, m.group(2)),'rb').read()).hexdigest()
                    line = m.group(1) + m.group(2) + '?hash=' + image_hash + m.group(3) + "\n"
            new_contents += line

        with open(build_adoc, 'w') as out_fh:
            out_fh.write(new_contents)
