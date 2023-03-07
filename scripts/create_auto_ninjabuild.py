#!/usr/bin/env python3

import os.path
import sys
import json
import re
import yaml

import ninja_syntax


def resolve_url(filename, relative_link):
    return os.path.normpath(os.path.join(os.path.dirname(filename), relative_link))

def scan_adoc(adoc_filename, apparent_filename, includes, src_images, dest_images, parents):
    parents.add(adoc_filename)
    # look for image files
    with open(os.path.join(input_dir, adoc_filename)) as fh:
        contents = fh.read()
        includes[adoc_filename] = set()
        joinee_dir = os.path.dirname(adoc_filename)
        # look for includes
        for include in re.findall(r'(?:^|\n)include::(.+?)\[\](?:\n|$)', contents):
            include_adoc = os.path.join(joinee_dir, include)
            if include_adoc in parents:
                raise Exception("{} includes {} which creates an infinite loop".format(adoc_filename, include_adoc))
            includes[adoc_filename].add(include_adoc)
            scan_adoc(include_adoc, apparent_filename, includes, src_images, dest_images, parents.copy())
        # look for image files
        for image in re.findall(r'image::?(.+?)\[.*\]', contents):
            if not (image.startswith('http:') or image.startswith('https:')):
                image_filename = resolve_url(adoc_filename, image)
                dest_image = resolve_url(apparent_filename, image)
                if dest_image in dest_images and dest_images[dest_image] != image_filename:
                    raise Exception("{} and {} would both end up as {}".format(dest_images[dest_image], image_filename, dest_image))
                src_images[image_filename] = dest_image
                dest_images[dest_image] = image_filename

def add_entire_directory(tab_dir, dir_path, pages_set, src_images, dest_images):
    #print("Adding all files from {} directory".format(tab_dir))
    for f in os.listdir(tab_dir):
        if os.path.isfile(os.path.join(tab_dir, f)):
            if f.endswith(".adoc"):
                pages_set.add(os.path.join(dir_path, f))
            elif f.endswith(".png"):
                image_filename = os.path.join(dir_path, f)
                dest_image = image_filename
                if dest_image in dest_images and dest_images[dest_image] != image_filename:
                    raise Exception("{} and {} would both end up as {}".format(dest_images[dest_image], image_filename, dest_image))
                src_images[image_filename] = dest_image
                dest_images[dest_image] = image_filename

if __name__ == "__main__":
    index_json = sys.argv[1]
    config_yaml = sys.argv[2]
    input_dir = sys.argv[3]
    if not os.path.exists(input_dir):
        raise Exception("{} doesn't exist".format(input_dir))
    scripts_dir = sys.argv[4]
    output_dir = sys.argv[5]
    adoc_includes_dir = sys.argv[6]
    assets_dir = sys.argv[7]
    doxygen_pico_sdk_build_dir = sys.argv[8]
    if not os.path.exists(doxygen_pico_sdk_build_dir):
        raise Exception("{} doesn't exist".format(doxygen_pico_sdk_build_dir))
    redirects_dir = sys.argv[9]
    images_dir = sys.argv[10]
    output_ninjabuild = sys.argv[11]

    global_images = ['full-sized/Datasheets.png', 'full-sized/PIP.png', 'full-sized/Tutorials.png', 'full-sized/Forums.png']

    # Read _config.yml
    with open(config_yaml) as config_fh:
        site_config = yaml.safe_load(config_fh)

    category_pages = set([
        ('index.adoc', site_config['title']),
        ('404.adoc', site_config['title'])
    ])
    doc_pages = set()
    page_images = set()
    srcimages2destimages = {}
    destimages2srcimages = {} # used for detecting filename conflicts
    static_pages = set()

    # Read index.json
    with open(index_json) as json_fh:
        data = json.load(json_fh)
        for tab in data['tabs']:
            assert 'title' in tab
            # either both present, or both missing
            assert ('path' in tab) == ('subitems' in tab)
            if 'path' in tab:
                # category (boxes) page
                category_pages.add((os.path.join(tab['path'], 'index.adoc'), '{} - {}'.format(site_config['title'], tab['title'])))
                # build_adoc
                if 'subitems' in tab:
                    for subitem in tab['subitems']:
                        if 'subpath' in subitem:
                            doc_pages.add(os.path.join(tab['path'], subitem['subpath']))
                        if 'image' in subitem:
                            page_images.add(subitem['image'])
            elif 'from_json' in tab:
                tab_dir = os.path.join(input_dir, tab['directory'])
                if os.path.exists(tab_dir):
                    # category (boxes) page
                    category_pages.add((os.path.join(tab['directory'], 'index.adoc'), '{} - {}'.format(site_config['title'], tab['title'])))
                    # recursively add entire directory
                    add_entire_directory(tab_dir, tab['directory'], static_pages, srcimages2destimages, destimages2srcimages)
                    # add all box images as well
                    tab_key = tab['directory']
                    if tab_key == 'pico-sdk':
                        page_images.add('full-sized/SDK-Intro.png')
                    all_images = os.listdir(os.path.join(images_dir, "full-sized"))
                    available_images = [f for f in all_images if f.startswith(tab_key+"_")]
                    if len(available_images) > 0:
                        for img in available_images:
                            page_images.add(os.path.join('full-sized', img))
                    else:
                        page_images.add('placeholder/placeholder_square.png')
            else:
                raise Exception("Tab '{}' in '{}' has neither '{}' nor '{}'".format(tab['title'], index_json, 'path', 'from_json'))

    for img in global_images:
        page_images.add(img)

    # Write rules to autogenerate files and copy adoc files
    with open(output_ninjabuild, 'w') as fh:
        ninja = ninja_syntax.Writer(fh, width=0)
        ninja.comment("This file is autogenerated, do not edit.")
        ninja.newline()
        ninja.variable('src_dir', input_dir)
        ninja.variable('out_dir', output_dir)
        ninja.variable('inc_dir', adoc_includes_dir)
        ninja.variable('scripts_dir', scripts_dir)
        ninja.variable('redirects_dir', redirects_dir)
        ninja.variable('documentation_index', index_json)
        ninja.variable('output_index', os.path.join(output_dir, "_data", "index.json"))
        ninja.variable('site_config', config_yaml)
        ninja.variable('doxyfile', os.path.join(doxygen_pico_sdk_build_dir, "docs", "Doxyfile"))
        ninja.newline()

        targets = []
        for page, title in sorted(category_pages):
            dest = os.path.join('$out_dir', page)
            ninja.build(dest, 'create_categories_page', variables={'title': title})
            targets.append(dest)

        if targets:
            ninja.default(targets)
            targets = []
            ninja.newline()

        all_doc_sources = []
        join_files = dict() # of sets
        # documentation pages
        for page in doc_pages:
            # find includes and images
            scan_adoc(page, page, join_files, srcimages2destimages, destimages2srcimages, set())
        #print(join_files)
        for page in sorted(doc_pages):
            for include in sorted(join_files[page]):
                source = os.path.join('$src_dir', include)
                if source not in all_doc_sources:
                    all_doc_sources.append(source)
                    dest = os.path.join('$inc_dir', include)
                    extra_sources = ['$scripts_dir/create_build_adoc_include.py', '$site_config', '$GITHUB_EDIT_TEMPLATE']
                    ninja.build(dest, 'create_build_adoc_include', source, extra_sources)
                    targets.append(dest)

            source = os.path.join('$src_dir', page)
            if source not in all_doc_sources:
                all_doc_sources.append(source)
                dest = os.path.join('$out_dir', page)
                extra_sources = ['$scripts_dir/create_build_adoc.py', '$documentation_index', '$site_config', '$GITHUB_EDIT_TEMPLATE']
                ninja.build(dest, 'create_build_adoc', source, extra_sources)
                targets.append(dest)
        if targets:
            ninja.default(targets)
            targets = []
            ninja.newline()

        include_files = dict() # of sets
        # static pages
        for page in static_pages:
            # find includes and images
            scan_adoc(page, page, include_files, srcimages2destimages, destimages2srcimages, set())
        #print(include_files)
        for page in sorted(static_pages):
            for include in sorted(include_files[page]):
                source = os.path.join('$src_dir', include)
                if source not in all_doc_sources:
                    raise Exception("{} was included in {} but it should have already been dealt with elsewhere".format(include, page))

            dest = os.path.join('$out_dir', page)
            source = os.path.join('$src_dir', page)
            extra_sources = ['$scripts_dir/create_build_adoc_doxygen.py', '$documentation_index', '$site_config', '$DOXYGEN_PICOSDK_INDEX_JSON']
            if source not in all_doc_sources:
                all_doc_sources.append(source)
                ninja.build(dest, 'create_build_adoc_doxygen', source, extra_sources)
                targets.append(dest)
        if targets:
            ninja.default(targets)
            targets = []
            ninja.newline()

        # images used on documentation pages
        for source in sorted(srcimages2destimages):
            dest = os.path.join('$out_dir', srcimages2destimages[source])
            source = os.path.join('$src_dir', source)
            ninja.build(dest, 'copy', source)
            targets.append(dest)
        if targets:
            ninja.default(targets)
            targets = []
            ninja.newline()

        # Images on boxes
        for image in sorted(page_images):
            dest = os.path.join('$out_dir', 'images', image)
            source = os.path.join('$DOCUMENTATION_IMAGES_DIR', image)
            ninja.build(dest, 'copy', source)
            targets.append(dest)
        if targets:
            ninja.default(targets)
            targets = []
            ninja.newline()

        # Jekyll-assets
        for root, dirs, files in os.walk(assets_dir):
            for asset in sorted(files):
                asset_filepath = os.path.relpath(os.path.join(root, asset), assets_dir)
                dest = os.path.join('$out_dir', asset_filepath)
                source = os.path.join(assets_dir, asset_filepath)
                ninja.build(dest, 'copy', source)
                targets.append(dest)
        if targets:
            ninja.default(targets)
            targets = []
            ninja.newline()

        # ToC data
        dest = os.path.join('$out_dir', '_data', 'nav.json')
        source = '$output_index'
        extra_sources = ['$scripts_dir/create_nav.py']
        extra_sources.extend(all_doc_sources)
        ninja.build(dest, 'create_toc', source, extra_sources)
        targets.append(dest)
        if targets:
            ninja.default(targets)
            targets = []
            ninja.newline()

        # supplemental data
        dest = os.path.join('$out_dir', '_data', 'supplemental.json')
        source = '$doxyfile'
        extra_sources = ['$scripts_dir/create_output_supplemental_data.py']
        ninja.build(dest, 'create_output_supplemental_data', source, extra_sources)
        targets.append(dest)
        if targets:
            ninja.default(targets)
            targets = []
            ninja.newline()

        # Redirects & htaccess
        dest = os.path.join('$out_dir', '.htaccess')
        source = '$HTACCESS_EXTRA'
        extra_sources = ['$scripts_dir/create_htaccess.py']
        for file in sorted(os.listdir(redirects_dir)):
            if os.path.splitext(file)[1] == '.csv':
                extra_sources.append(os.path.join('$redirects_dir', file))
        ninja.build(dest, 'create_htaccess', source, extra_sources)
        targets.append(dest)
        if targets:
            ninja.default(targets)
            targets = []
            ninja.newline()
