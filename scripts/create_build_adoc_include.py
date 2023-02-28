#!/usr/bin/env python3

import sys
import os
import re
import yaml


def check_no_markdown(filename):
    with open(filename) as fh:
        asciidoc = fh.read()
        if re.search('```\n.*?\n```', asciidoc):
            raise Exception("{} uses triple-backticks for markup - please use four-hyphens instead".format(filename))
        # strip out code blocks
        asciidoc = re.sub('----\n.*?\n----', '', asciidoc, flags=re.DOTALL)
        # strip out pass-through blocks
        asciidoc = re.sub('\+\+\+\+\n.*?\n\+\+\+\+', '', asciidoc, flags=re.DOTALL)
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
        edit_text = re.sub('{{\s*(\w+)\s*}}', lambda m: template_vars[m.group(1)], edit_template)

    with open(src_adoc) as in_fh:
        new_contents = ''
        seen_header = False
        for line in in_fh.readlines():
            if line.startswith('== '):
                if not seen_header:
                    seen_header = True
                    if github_edit is not None:
                        line += edit_text + "\n\n"
            new_contents += line

        with open(build_adoc, 'w') as out_fh:
            out_fh.write(new_contents)
