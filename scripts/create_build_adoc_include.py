#!/usr/bin/env python3

import sys
import os
import yaml

if __name__ == "__main__":
    config_yaml = sys.argv[1]
    src_adoc = sys.argv[2]
    build_adoc = sys.argv[3]

    with open(config_yaml) as config_fh:
        site_config = yaml.safe_load(config_fh)
    with open(src_adoc) as in_fh:
        new_contents = ''
        seen_header = False
        for line in in_fh.readlines():
            if line.startswith('== '):
                if not seen_header:
                    seen_header = True
                    line += "Edit this {}[on GitHub]\n\n".format(os.path.join(site_config['githuburl'], 'blob', site_config['githubbranch_edit'], src_adoc))
            new_contents += line

        with open(build_adoc, 'w') as out_fh:
            out_fh.write(new_contents)
