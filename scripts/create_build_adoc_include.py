#!/usr/bin/env python3

import sys
import os
import re
import yaml

from create_build_adoc import check_no_markdown, append_query_hash_to_all_images, check_invalid_urls


if __name__ == "__main__":
    config_yaml = sys.argv[1]
    github_edit = sys.argv[2]
    src_adoc = sys.argv[3]
    build_adoc = sys.argv[4]

    with open(src_adoc) as fh:
        asciidoc_text = fh.read()

    check_no_markdown(src_adoc, asciidoc_text)

    asciidoc_text = append_query_hash_to_all_images(src_adoc, asciidoc_text)

    with open(config_yaml) as config_fh:
        site_config = yaml.safe_load(config_fh)

    check_invalid_urls(src_adoc, asciidoc_text, site_config['url'], site_config['githuburl'])

    with open(github_edit) as edit_fh:
        edit_template = edit_fh.read()
        template_vars = {
            'github_edit_link': os.path.join(site_config['githuburl'], 'blob', site_config['githubbranch'], src_adoc)
        }
        edit_text = re.sub(r'{{\s*(\w+)\s*}}', lambda m: template_vars[m.group(1)], edit_template)

    new_contents = ''
    seen_header = False
    for line in asciidoc_text.split('\n'):
        line += '\n'
        if re.match('^=+ ', line) is not None:
            if not seen_header:
                seen_header = True
                if github_edit is not None:
                    line += edit_text + "\n\n"
        new_contents += line

    with open(build_adoc, 'w') as out_fh:
        out_fh.write(new_contents)
