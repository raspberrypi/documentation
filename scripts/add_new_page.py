#!/usr/bin/env python3

# Example usage:
#   scripts/add_new_page.py "My new HAT"
# will create documentation/asciidoc/accessories/my-new-hat.adoc and documentation/asciidoc/accessories/my-new-hat/about.adoc
#
#   scripts/add_new_page.py -b new-hat "My new HAT"
# will create documentation/asciidoc/accessories/new-hat.adoc and documentation/asciidoc/accessories/new-hat/about.adoc
#
#   scripts/add_new_page.py -b new-hat -s intro "My new HAT"
# will create documentation/asciidoc/accessories/new-hat.adoc and documentation/asciidoc/accessories/new-hat/intro.adoc
#
#   scripts/add_new_page.py -c services "Some extra Service"
# will create documentation/asciidoc/services/some-extra-service.adoc and documentation/asciidoc/services/some-extra-service/about.adoc
#
#   scripts/add_new_page.py -c services -b id -s signing_up "Raspberry Pi ID"
# will create documentation/asciidoc/services/id.adoc and documentation/asciidoc/services/id/signing_up.adoc

import argparse
import json
import os
import random
import re
import shutil
import sys

DOCUMENTATION_DIR = 'documentation'
INDEX_JSON = os.path.join(DOCUMENTATION_DIR, 'index.json')
IMAGES_DIR = os.path.join(DOCUMENTATION_DIR, 'images')
PLACEHOLDER_IMAGES_DIR = os.path.join(IMAGES_DIR, 'placeholder')
PLACEHOLDER_SHAPES = ('circle', 'square', 'triangle')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('-c', '--category', default='accessories')
    parser.add_argument('-b', '--basename')
    parser.add_argument('-s', '--subfile', default='about')
    args = parser.parse_args()
    print(args)

    name = args.name
    category = args.category
    basename = args.basename
    if not basename:
        basename = re.sub('\W', '-', name.lower())
    subfile = f"{args.subfile}.adoc"

    # Validate the category
    valid_categories = []
    with open(INDEX_JSON, 'r') as json_fh:
        json_contents = json.load(json_fh)
        for tab in json_contents["tabs"]:
            if 'from_json' in tab:
                continue
            valid_categories.append(tab['path'])
    if category not in valid_categories:
        raise Exception(f"Invalid category {category}. Choose from {valid_categories}")
    category_dir = os.path.join(DOCUMENTATION_DIR, 'asciidoc', category)
    if not os.path.exists(category_dir):
        raise Exception(f"{category_dir} doesn't exist")

    # Check the new page hasn't already been added
    new_dir = os.path.join(category_dir, basename)
    if os.path.isdir(new_dir):
        raise Exception(f"{new_dir} already exists")
    new_file = f"{new_dir}.adoc"
    if os.path.isfile(new_file):
        raise Exception(f"{new_file} already exists")
    new_subfile = os.path.join(new_dir, subfile)
    if os.path.isfile(new_subfile):
        raise Exception(f"{new_subfile} already exists")

    print(f"Will create {new_file} and {new_subfile}")
    # sys.exit(0)
    # Create the template AsciiDoc documentation
    os.mkdir(new_dir)
    with open(new_file, 'w') as fh:
        fh.write(f"include::{basename}/{subfile}[]\n")
    with open(new_subfile, 'w') as fh:
        fh.write(f"== About\n\nAll about {name} and why it's amazing")

    # Add the placeholder images
    shape = random.choice(PLACEHOLDER_SHAPES)
    shutil.copyfile(os.path.join(PLACEHOLDER_IMAGES_DIR, f"placeholder_{shape}-SMALL.png"), os.path.join(IMAGES_DIR, f"{basename}-SMALL.png"))
    shutil.copyfile(os.path.join(PLACEHOLDER_IMAGES_DIR, f"placeholder_{shape}.png"), os.path.join(IMAGES_DIR, 'full-sized', f"{basename}.png"))

    # And finally update the JSON which ties everything together
    with open(INDEX_JSON, 'r+') as json_fh:
        json_contents = json.load(json_fh)
        found = False
        for tab in json_contents["tabs"]:
            if tab['path'] == category:
                found = True
                tab["subitems"].append({
                    "title": name,
                    "description": f"Description of {name}",
                    "image": os.path.join('full-sized', f"{basename}.png"),
                    "subpath": f"{basename}.adoc",
                })
                break
        if not found: # this shouldn't ever happen, as we already validated the category earlier
            raise Exception(f"Couldn't find tab with path {category} in {INDEX_JSON}")
        json_fh.seek(0)
        json.dump(json_contents, json_fh, indent=4)

    print(f"Done. Use 'git status' and 'git diff' to see what has changed, and then add more content to\n {new_subfile}")

