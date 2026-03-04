#!/usr/bin/env python3

import sys
import os
import json
import re
import yaml
import hashlib


def check_no_markdown(filename, asciidoc):
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


# find all image references, append md5 hash at end to bust the cache if we change the image
def append_query_hash_to_all_images(filename, asciidoc):
    def _append_hash_to_image(srcfile, m):
        if m:
            tag = m.group(1)
            filename = m.group(2)
            caption = m.group(3)
            directory = os.path.dirname(os.path.abspath(srcfile))
            with open(os.path.join(directory, filename), 'rb') as image_fh:
                image_data = image_fh.read()
                image_hash = hashlib.md5(image_data).hexdigest()
                return tag + filename + '?hash=' + image_hash + caption
            # if image_hash couldn't be calculated, just return original input
            return tag + filename + caption

    return re.sub(r'(image::)(.+)(\[(?:.+)]\n?)', lambda m: _append_hash_to_image(filename, m), asciidoc)


def check_invalid_urls(filename, asciidoc, site_url, github_url):
    for m in re.finditer(r'(https?://[^\[\]:\s$]+)', asciidoc):
        url = m.group(1)
#        print(url)
        if url.startswith(site_url):
            raise Exception("{} has an absolute link to {} - please use a relative link instead".format(filename, url))
        elif url.startswith(github_url):
            raise Exception("{} has a link to {} - please use a (relative) link to the corresponding page on {} instead".format(filename, url, site_url))
        elif re.match(r"^https?://datasheets\.raspberrypi\.(?:com|org)", url):
            raise Exception("{} has a legacy link to {} - please use a PIP URL instead".format(filename, url))
        elif url.startswith("https://pip-assets.raspberrypi.com/") or re.match(r"^https?://pip\.raspberrypi\.com/(?:.+/)?documents/.+", url):
            if not re.match(r"^https://pip\.raspberrypi\.com/documents/RP-\d{6}-[A-Z]{2}(?:-[^-][-\w,\.%]+\.[a-z0-9]+)?$", url):
                raise Exception("{} has a PIP URL of {} - please update it to the https://pip.raspberrypi.com/documents/RP-NNNNNN-XY or https://pip.raspberrypi.com/documents/RP-NNNNNN-XY-some-filename.pdf format".format(filename, url))


if __name__ == "__main__":
    index_json = sys.argv[1]
    config_yaml = sys.argv[2]
    page_preamble = sys.argv[3]
    github_edit = sys.argv[4]
    src_adoc = sys.argv[5]
    includes_dir = sys.argv[6]
    build_adoc = sys.argv[7]

    output_subdir = os.path.basename(os.path.dirname(build_adoc))
    adoc_filename = os.path.basename(build_adoc)

    with open(src_adoc) as fh:
        asciidoc_text = fh.read()

    check_no_markdown(src_adoc, asciidoc_text)

    asciidoc_text = append_query_hash_to_all_images(src_adoc, asciidoc_text)

    index_title = None
    with open(index_json) as json_fh:
        data = json.load(json_fh)
        for tab in data['tabs']:
            if 'path' in tab and tab['path'] == output_subdir:
                for subitem in tab['subitems']:
                    if 'subpath' in subitem and subitem['subpath'] == adoc_filename:
                        index_title = subitem['title']
                        break
                if index_title is not None:
                    break
    if index_title is None:
        raise Exception("Couldn't find title for {} in {}".format(os.path.join(output_subdir, adoc_filename), index_json))

    with open(config_yaml) as config_fh:
        site_config = yaml.safe_load(config_fh)

    check_invalid_urls(src_adoc, asciidoc_text, site_config['url'], site_config['githuburl'])

    with open(github_edit) as edit_fh:
        edit_template = edit_fh.read()
        template_vars = {
            'github_edit_link': os.path.join(site_config['githuburl'], 'blob', site_config['githubbranch'], src_adoc)
        }
        edit_text = re.sub(r'{{\s*(\w+)\s*}}', lambda m: template_vars[m.group(1)], edit_template)

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
    seen_header = False
    for line in asciidoc_text.split('\n'):
        line += '\n'
        if re.match('^=+ ', line) is not None:
            if not seen_header:
                seen_header = True
                if github_edit is not None:
                    line += edit_text + "\n\n"
        else:
            m = re.match(r'^(include::)(.+)(\[\]\n?)$', line)
            if m:
                line = m.group(1) + os.path.join('{includedir}/{parentdir}', m.group(2)) + m.group(3)
        new_contents += line

    with open(build_adoc, 'w') as out_fh:
        out_fh.write(new_contents)
