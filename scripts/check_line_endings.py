#!/usr/bin/env python3

import os
import sys

SEARCH_PATHS = set(["documentation/asciidoc"])
SEARCH_EXTENSIONS = set([".adoc"])

def contains_cr(filepath):
    with open(filepath, "rb") as fh:
        return b"\r" in fh.read()

if __name__ == "__main__":
    bad_files = set()
    for path in SEARCH_PATHS:
        for root, dirs, files in os.walk(path):
            for name in files:
                if os.path.splitext(name)[1] in SEARCH_EXTENSIONS:
                    filepath = os.path.join(root, name)
                    if contains_cr(filepath):
                        bad_files.add(filepath)

    if bad_files:
        print("The following files contain a CR character (please convert them to UNIX line-endings):")
        print("\n".join(sorted(bad_files)))
        sys.exit(1)
