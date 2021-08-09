#!/usr/bin/env python3

import sys
import os
import json

if __name__ == "__main__":
    index_json = sys.argv[1]
    src_dir = sys.argv[2]
    src_adoc = sys.argv[3]
    build_adoc = sys.argv[4]
    output_path = os.path.basename(os.path.dirname(build_adoc))
    adoc_filename = os.path.basename(build_adoc)

    index_title = None
    with open(index_json) as json_fh:
        data = json.load(json_fh)
        for tab in data['tabs']:
            if 'path' in tab and tab['path'] == output_path:
                for subitem in tab['subitems']:
                    if 'subpath' in subitem and subitem['subpath'] == adoc_filename:
                        index_title = subitem['title']
                        break
                if index_title is not None:
                    break
    if index_title is None:
        raise Exception("Couldn't find title for {} in {}".format(os.path.join(output_path, adoc_filename), index_json))

    with open(build_adoc, 'w') as out_fh:
        out_fh.write(""":parentdir: {}
:page-layout: docs
:includedir: {}
:doctitle: Raspberry Pi Documentation - {}

include::{{includedir}}/{{parentdir}}/{}[]
""".format(output_path, src_dir, index_title, adoc_filename))
