#!/usr/bin/env python3

import sys
import re
import os
#import html
from bs4 import BeautifulSoup

# walk the combined output.
# for each function:
# check if it is in the output for one chip, or both
# if for only one chip, add a role to that section accordingly.

# instead of searching every xml every time, make a list of available functions in each xml
def compile_id_list(xml_content):
    # get any element that has an id
    els = xml_content.find_all(id=True)
    id_list = [x["id"] for x in els]
    return id_list

# Unused code - but kept in case we need it in future
#def insert_example_code_from_file(combined_content):
#    els = combined_content.doxygen.find_all("programlisting")
#    all_examples = {}
#    # get the examples path
#    examples_path = re.sub(r"/scripts/.+$", "/lib/pico-examples", os.path.realpath(__file__))
#    # get a recursive list of all files in examples
#    for f in os.walk(examples_path):
#        for filename in f[2]:
#            if filename in all_examples:
#                all_examples[filename].append(os.path.join(f[0], filename))
#            else:
#                all_examples[filename] = [os.path.join(f[0], filename)]
#    for el in els:
#        if el.get("filename") is not None:
#            filename = el.get("filename")
#            # find the file here or in examples
#            if filename in all_examples:
#                with open(all_examples[filename][0]) as f:
#                    example_content = f.read()
#                example_lines = example_content.split("\n")
#                for line in example_lines:
#                    codeline = BeautifulSoup("<codeline>"+html.escape(line)+"</codeline>", 'xml')
#                    el.append(codeline)
#    return combined_content

def walk_and_tag_xml_tree(el, output_contexts, all_contexts):
    """
    Process an individual xml file, adding context-specific tags as needed.

    For performance purposes (to avoid traversing multiple dicts for every element),
    we use element IDs as the key, and the contexts it belongs to as the value.
    Thus, output_contexts will look something like this:
    {
        "group__hardware__gpio_1gaecd01f57f1cac060abe836793f7bea18": [
            "PICO_RP2040",
            "FOO"
        ],
        "group__hardware__gpio_1ga7becbc8db22ff0a54707029a2c0010e6": [
            "PICO_RP2040"
        ],
        "group__hardware__gpio_1ga192335a098d40e08b23cc6d4e0513786": [
            "PICO_RP2040"
        ],
        "group__hardware__gpio_1ga8510fa7c1bf1c6e355631b0a2861b22b": [
            "FOO",
            "BAR"
        ],
        "group__hardware__gpio_1ga5d7dbadb2233e2e6627e9101411beb27": [
            "FOO"
        ]
    }
    """
    targets = []
    if el.get('id') is not None:
        myid = el["id"]
        if myid in output_contexts:
            targets = output_contexts[myid]
        # if this content is in all contexts, no label is required
        if len(targets) > 0 and len(targets) < len(all_contexts):
            el["role"] = "contextspecific"
            el["tag"] = ', '.join(targets)
            if len(targets) > 1:
                el["type"] = "multi"
            else:
                el["type"] = targets[0]
        # only check nested children if the parent has NOT been tagged as context-specific
        else:
            # for child in el.iterchildren():
            for child in el.find_all(True, recursive=False):
                walk_and_tag_xml_tree(child, output_contexts, all_contexts)
    else:
        for child in el.find_all(True, recursive=False):
            walk_and_tag_xml_tree(child, output_contexts, all_contexts)
    return

def postprocess_doxygen_xml_file(combined_xmlfile, xmlfiles, output_context_paths):
    """
    Process an individual xml file, adding context-specific tags as needed.

    xmlfiles will look something like this:
    {
        "PICO_RP2040": "/path/to/PICO_RP2040/myfilename.xml",
        "FOO": "/path/to/FOO/myfilename.xml"
    }
    """
    output_contexts = {}
    for item in xmlfiles:
        label = item
        # parse the xml file
        with open(xmlfiles[item], encoding="utf-8") as f:
            xml_content = BeautifulSoup(f, 'xml')
        # compile a list of all element ids within the file
        id_list = compile_id_list(xml_content.doxygen)
        # create the map of ids and their contexts (see example above)
        for myid in id_list:
            if myid in output_contexts:
                output_contexts[myid].append(label)
            else:
                output_contexts[myid] = [label]
    with open(combined_xmlfile, encoding="utf-8") as f:
        combined_content = BeautifulSoup(f, 'xml')
    # start with top-level children, and then walk the tree as appropriate
    els = combined_content.doxygen.find_all(True, recursive=False)
    for el in els:
        walk_and_tag_xml_tree(el, output_contexts, list(output_context_paths.keys()))
    # I think this was only needed because the PICO_EXAMPLES_PATH was wrong in the Makefile
    #combined_content = insert_example_code_from_file(combined_content)
    return str(combined_content)

def postprocess_doxygen_xml(xml_path):
    """
    Expectation is that xml for each context will be generated
    within a subfolder titled with the context name, e.g.:
    - doxygen_build/
      - combined/
      - PICO_RP2040/
      - FOO/
    """
    # collect a list of all context-specific subdirs
    skip = ["index.xml", "Doxyfile.xml"]
    output_context_paths = {}
    combined_output_path = None
    for item in list(filter(lambda x: os.path.isdir(os.path.join(xml_path, x)), os.listdir(xml_path))):
        if item == "combined":
            # if doxygen ever changes the output path for the xml, this will need to be updated
            combined_output_path = os.path.join(xml_path, item, "docs", "doxygen", "xml")
        else:
            # same as above
            output_context_paths[item] = os.path.join(xml_path, item, "docs", "doxygen", "xml")
    # we need to process all generated xml files
    for combined_xmlfile in list(filter(lambda x: re.search(r'\.xml$', x) is not None, os.listdir(combined_output_path))):
        # skip the index -- it's just a listing
        if combined_xmlfile not in skip:
            xmlfiles = {}
            # get all context-specific versions of this file
            for context in output_context_paths:
                if os.path.isfile(os.path.join(output_context_paths[context], combined_xmlfile)):
                    xmlfiles[context] = os.path.join(output_context_paths[context], combined_xmlfile)
            combined_content = postprocess_doxygen_xml_file(os.path.join(combined_output_path, combined_xmlfile), xmlfiles, output_context_paths)
            # write the output
            with open(os.path.join(combined_output_path, combined_xmlfile), 'w') as f:
                f.write(combined_content)
    return

if __name__ == '__main__':
    xml_path = sys.argv[1]
    file_path = os.path.realpath(__file__)
    # splitting thse subs into two parts to make testing easier
    # xml_path = re.sub(r'/documentation-toolchain/.*?$', "/"+xml_path, re.sub(r'/lib/', "/", file_path))
    postprocess_doxygen_xml(xml_path)
