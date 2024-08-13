#!/usr/bin/env python3

import re
import sys
import os
import json

def cleanup_text_page(adoc_file, output_adoc_path, link_targets):
    filename = os.path.basename(adoc_file)
    with open(adoc_file) as f:
        adoc_content = f.read()
    # remove any errant spaces before anchors
    adoc_content = re.sub(r'( +)(\[\[[^[]*?\]\])', "\\2", adoc_content)
    # collect link targets
    for line in adoc_content.split('\n'):
        link_targets = collect_link_target(line, filename)
    with open(adoc_file, 'w') as f:
        f.write(adoc_content)
    return link_targets

def collect_link_target(line, chapter_filename):
    # collect a list of all link targets, so we can fix internal links
    l = re.search(r'(#)([^,\]]+)([,\]])', line)
    if l is not None:
        link_targets[l.group(2)] = chapter_filename
    return link_targets

def resolve_links(adoc_file, link_targets):
    filename = os.path.basename(adoc_file)
    with open(adoc_file) as f:
        adoc_content = f.read()
    output_content = []
    for line in adoc_content.split('\n'):
        # e.g., <<examples_page,here>>
        m = re.search("(<<)([^,]+)(,?[^>]*>>)", line)
        if m is not None:
            target = m.group(2)
            # only resolve link if it points to another file
            if target in link_targets and link_targets[target] != filename:
                new_target = link_targets[target]+"#"+target
                line = re.sub("(<<)([^,]+)(,?[^>]*>>)", f"\\1{new_target}\\3", line)
        output_content.append(line)
    with open(adoc_file, 'w') as f:
        f.write('\n'.join(output_content))
    return

def build_json(sections, output_path):
    json_path = os.path.join(output_path, "picosdk_index.json")
    with open(json_path, 'w') as f:
        f.write(json.dumps(sections, indent="\t"))
    return

def tag_content(adoc_content):
    # this is dependent on the same order of attributes every time
    ids_to_tag = re.findall(r'(\[#)(.*?)(,.*?contextspecific,tag=)(.*?)(,type=)(.*?)(\])', adoc_content)
    for this_id in ids_to_tag:
        tag = re.sub("PICO_", "", this_id[3])
        img = f" [.contexttag {tag}]*{tag}*"
        # `void <<group_hardware_gpio_1ga5d7dbadb2233e2e6627e9101411beb27,gpio_rp2040>> ()`:: An rp2040 function.
        adoc_content = re.sub(rf'(\n`.*?<<{this_id[1]},.*?`)(::)', f"\\1{img}\\2", adoc_content)
        # |<<group_hardware_base,hardware_base>>\n|Low-level types and (atomic) accessors for memory-mapped hardware registers.
        adoc_content = re.sub(rf'(\n\|<<{this_id[1]},.*?>>\n\|.*?)(\n)', f"\\1{img}\\2", adoc_content)
    # [#group_cyw43_ll_1ga0411cd49bb5b71852cecd93bcbf0ca2d,role=contextspecific,tag=PICO_RP2040,type=PICO_RP2040]\n=== anonymous enum
    HEADING_RE = re.compile(r'(\[#.*?role=contextspecific.*?tag=P?I?C?O?_?)(.*?)(,.*?\]\s*?\n\s*=+\s+\S*?)(\n)')
    # [#group_cyw43_ll_1ga0411cd49bb5b71852cecd93bcbf0ca2d,role=h6 contextspecific,tag=PICO_RP2040,type=PICO_RP2040]\n*anonymous enum*
    H6_HEADING_RE = re.compile(r'(\[#.*?role=h6 contextspecific.*?tag=P?I?C?O?_?)(.*?)(,.*?\]\s*?\n\s*\*\S+.*?)(\n)')
    # [#group_cyw43_ll_1ga0411cd49bb5b71852cecd93bcbf0ca2d,role=h6 contextspecific,tag=PICO_RP2040,type=PICO_RP2040]\n----
    NONHEADING_RE = re.compile(r'(\[#.*?role=h?6?\s?contextspecific.*?tag=P?I?C?O?_?)(.*?)(,.*?\]\s*?\n\s*[^=\*])')
    adoc_content = re.sub(HEADING_RE, f'\\1\\2\\3 [.contexttag \\2]*\\2*\n', adoc_content)
    adoc_content = re.sub(H6_HEADING_RE, f'\\1\\2\\3 [.contexttag \\2]*\\2*\n', adoc_content)
    adoc_content = re.sub(NONHEADING_RE, f'[.contexttag \\2]*\\2*\n\n\\1\\2\\3', adoc_content)
    return adoc_content

def postprocess_doxygen_adoc(adoc_file, output_adoc_path, link_targets):
    output_path = re.sub(r'[^/]+$', "", adoc_file)
    sections = [{
        "group_id": "index_doxygen",
        "name": "Introduction",
        "description": "An introduction to the Pico SDK",
        "html": "index_doxygen.html",
        "subitems": []
    }]
    with open(adoc_file) as f:
        adoc_content = f.read()
    # first, lets add any tags
    adoc_content = tag_content(adoc_content)
    # now split the file into top-level sections:
    # toolchain expects all headings to be two levels lower
    adoc_content = re.sub(r'(\n==)(=+ \S+)', "\n\\2", adoc_content)
    # then make it easier to match the chapter breaks
    adoc_content = re.sub(r'(\[#.*?,reftext=".*?"\])(\s*\n)(= )', "\\1\\3", adoc_content)
    # find all the chapter descriptions, to use later
    descriptions = re.findall(r'(\[#.*?,reftext=".*?"\])(= .*?\n\s*\n)(.*?)(\n)', adoc_content)
    CHAPTER_START_RE = re.compile(r'(\[#)(.*?)(,reftext=".*?"\]= )(.*?$)')
    # check line by line; if the line matches our chapter break,
    # then pull all following lines into the chapter list until a new match.
    chapter_filename = "all_groups.adoc"
    current_chapter = None
    chapter_dict = {}
    counter = 0
    for line in adoc_content.split('\n'):
        link_targets = collect_link_target(line, chapter_filename)
        m = CHAPTER_START_RE.match(line)
        if m is not None:
            # write the previous chapter
            if current_chapter is not None:
                with open(chapter_path, 'w') as f:
                    f.write('\n'.join(current_chapter))
            # start the new chapter
            current_chapter = []
            # set the data for this chapter
            group_id = re.sub("^group_+", "", m.group(2))
            chapter_filename = group_id+".adoc"
            chapter_path = os.path.join(output_path, chapter_filename)
            chapter_dict = {
                "group_id": group_id,
                "html": group_id+".html",
                "name": m.group(4),
                "subitems": [],
                "description": descriptions[counter][2]
            }
            sections.append(chapter_dict)
            # re-split the line into 2
            start_line = re.sub("= ", "\n= ", line)
            current_chapter.append(start_line)
            counter += 1
        else:
            current_chapter.append(line)
    # write the last chapter
    if current_chapter is not None:
        with open(chapter_path, 'w') as f:
            f.write('\n'.join(current_chapter))
    build_json(sections, output_path)
    os.remove(adoc_file)
    return link_targets

if __name__ == '__main__':
    output_adoc_path = sys.argv[1]
    adoc_files = [f for f in os.listdir(output_adoc_path) if re.search(".adoc", f) is not None]
    link_targets = {}
    for adoc_file in adoc_files:
        adoc_filepath = os.path.join(output_adoc_path, adoc_file)
        if re.search("all_groups.adoc", adoc_file) is not None:
            link_targets = postprocess_doxygen_adoc(adoc_filepath, output_adoc_path, link_targets)
        else:
            link_targets = cleanup_text_page(adoc_filepath, output_adoc_path, link_targets)
    # now that we have a complete list of all link targets, resolve all internal links
    adoc_files = [f for f in os.listdir(output_adoc_path) if re.search(".adoc", f) is not None]
    for adoc_file in adoc_files:
        adoc_filepath = os.path.join(output_adoc_path, adoc_file)
        resolve_links(adoc_filepath, link_targets)
