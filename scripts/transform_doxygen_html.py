#!/usr/bin/env python3

import json
import os
import sys
import re
import random
import string
import copy
import hashlib

from lxml import etree

# TO DO:
# do internal href links need to be updated?

def get_all_text(node):
  text = node.text if node.text else None
  if text:
    yield text
  for child in node:
    yield from get_all_text(child)
  tail = node.tail if node.tail else None
  if tail:
    yield tail

def stringify(lxml_content):
  html_string = etree.tostring(lxml_content, pretty_print=True, encoding='UTF-8').decode('utf-8')
  return html_string

def write_output(filepath, content):
  f = open(filepath, 'w')
  f.write(content)
  f.close()
  return

def make_hash(string):
  hash_object = hashlib.sha1(bytes(string, 'utf-8'))
  new_hash = hash_object.hexdigest()
  if len(new_hash) > 20:
    new_hash = new_hash[:20]
  return new_hash

def add_ids(root, html_file):
  els = root.xpath(".//body//*[not(@id)]")
  counter = 0
  for el in els:
    hash_string = str(counter)+html_file+''.join(get_all_text(el))
    newid = make_hash(hash_string)
    newid = "rpip" + newid
    el.set("id", newid)
    counter += 1
  return root

def strip_attribute(att, root):
  els = root.xpath(".//*[@"+att+"]")
  for el in els:
    el.attrib.pop(att)
  return root

def make_attribute_selector(sel, item):
  try:
    atts = []
    for att in item["attributes"]:
      # if we've got a wildcard, this should be a "contains" selector,
      # e.g. [contains(@class,'foo')]:
      contains = False
      for att_value in att["value"]:
        if "*" in att_value:
          contains = True
      if contains == True:
        val = re.sub("\*", "", " ".join(att["value"]))
        atts.append("contains(@" + att["name"] + ",'" + val + "')")
      else:
        # otherwise it's a normal attribute selector
        atts.append("@" + att["name"] + "='" + " ".join(att["value"]) + "'")
    if len(atts) > 0:
      att_string = " and ".join(atts)
      sel = sel + "[" + att_string + "]"
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return sel

def make_parent_selector(sel, item):
  try:
    if len(item["parents"]) > 0:
      # sort the parents by level
      # add each parent to the selector based on level
      parent_sel = ""
      sorted_parents = list(reversed(sorted(item["parents"], key=lambda d: d['level'])))
      for ix, parent in enumerate(sorted_parents):
        # now add the parent element to the selector
        parent_sel = parent_sel + parent["element"]
        parent_sel = make_attribute_selector(parent_sel, parent)
        if len(sorted_parents) > ix+1:
          next_ix = ix+1
          level = parent["level"] - sorted_parents[next_ix]["level"] - 1
        else:
          level = parent["level"]
        if level > 0:
          for i in range(level):
            parent_sel = parent_sel + "/*"
        parent_sel = parent_sel + "/"
      sel = sel + parent_sel
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return sel

def make_selector(item, is_child=False):
  sel = None
  try:
    if is_child == True:
      sel = "./"
    else:
      sel = ".//"
    # add parent selectors
    sel = make_parent_selector(sel, item)
    sel = sel + item["element"]
    sel = make_attribute_selector(sel, item)
    sel = sel + "[not(@data-processed='true')]"
    # add child selectors
    # TO DO
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return sel

def make_new_element(item):
  new_el = None
  # construct the new element and children from the mapping
  try:
    new_el = etree.Element(item["element"])
    for att in item["attributes"]:
      new_el.set(att["name"], ' '.join(att["value"]))
    new_el.set("data-processed", "true")
    sorted_children = sorted(item["children"], key=lambda d: d['position'])
    for child in sorted_children:
      new_child = make_new_element(child)
      new_el.append(new_child)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return new_el

def make_tree(item):
  new_tree = None
  # construct the complete element tree from the mapping
  try:
    tree = item["output"]["tree"]
    if len(tree) > 0:
      sorted_tree = sorted(tree, key=lambda d: d['position'])
      # build an element
      for tree_el in sorted_tree:
        new_tree = make_new_element(tree_el)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return new_tree

def add_content_to_tree(new_tree, match):
  try:
    # preserve the same id, just in case
    new_tree.set("id", match.get("id"))
    # also preserve the original parent id
    parent = match.getparent()
    if parent is not None and parent.get("id") is not None:
      new_tree.set("data-parent-id", parent.get("id"))
    # figure out where to insert any children
    # (this is configured in the json mapping)
    target = new_tree.find(".//*[@data-target='true']")
    if target is None:
      target = new_tree
    target.text = match.text
    target.tail = match.tail
    target.set("data-target-for", match.get("id"))
    # children will get processed separately
    # add any children inside the target
    for child in match.findall("./*"):
      target.append(child)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return new_tree

def transform_element(item, root, is_child=False):
  try:
    # build the selector for the xpath
    sel = make_selector(item["input"], is_child)
    if sel is not None:
      matches = root.xpath(sel)
      for match in matches:
        # first process any mapped children
        if "child_mappings" in item["input"] and len(item["input"]["child_mappings"]) > 0:
          for child_item in item["input"]["child_mappings"]:
            match = transform_element(child_item, match, True)
        new_tree = make_tree(item)
        if new_tree is not None:
          # set attributes, add text/tail, and add children
          new_tree = add_content_to_tree(new_tree, match)
          # add the new tree to the document
          match.addnext(new_tree)
          # remove the old element
          match.getparent().remove(match)
        else:
          # if there is no tree, the element should be removed
          # first, preserve any children:
          for child in reversed(match.findall("./*")):
            match.addnext(child)
          # handle the tail if needed
          if match.tail is not None and re.search("\S", match.tail) is not None:
            prev = match.getprevious()
            if prev is not None:
              prev.tail = prev.tail + match.tail if prev.tail is not None else match.tail
            else:
              parent = match.getparent()
              parent.text = parent.text + match.tail if parent.text is not None else match.tail
          # then remove the element
          match.getparent().remove(match)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root

def fix_duplicate_ids(root, html_file):
  try:
    existing = []
    matches = root.xpath(".//*[contains(@id, 'rpip')]")
    counter = 0
    for match in matches:
      myid = match.get("id")
      if myid in existing:
        id_string = str(counter)+html_file+''.join(get_all_text(match))
        newid = make_hash(id_string)
        newid = "rpip"+newid
        match.set("id", newid)
        existing.append(newid)
        counter += 1
      else:
        existing.append(myid)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root

def fix_internal_links(root, html_file, updated_links):
  try:
    # first let's make sure internal links are all unique
    matches = root.xpath(".//a[contains(@href, '#') and not(@data-adjusted)]")
    while len(matches) > 0:
      match = matches[0]
      href = match.get("href")
      if re.match("^#", href) is not None and len(href) < 30:
        # make a new hash string
        hash_string = html_file+''.join(get_all_text(match))+match.get("href")
        newid = make_hash(hash_string)
        newid = "ga" + newid
        updated_links[html_file+href] = html_file+"#"+newid
        match.set("href", "#"+newid)
        match.set("data-adjusted", "true")
        links = root.xpath(".//a[@href='#"+href+"']")
        for link in links:
          link.set("href", "#"+newid)
          link.set("data-adjusted", "true")
        anchor_id = re.sub("^#", "", href)
        anchors = root.xpath(".//*[@id='"+anchor_id+"']")
        for anchor in anchors:
          anchor.set("id", newid)
      else:
        match.set("data-adjusted", "true")
      matches = root.xpath(".//a[contains(@href, '#') and not(@data-adjusted)]")
    # then we'll adjust them
    matches = root.xpath(".//a[contains(@href, '"+html_file+"#')]")
    for match in matches:
      href = match.get("href")
      new_href = re.sub(html_file, "", href)
      match.set("href", new_href)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root, updated_links

def find_item_in_dict(k,v,filename):
  found = False
  try:
    if k == filename:
      found = True
    elif len(v) > 0:
      for sk, sv in v.items():
        found = find_item_in_dict(sk,sv,filename)
        if found == True:
          break
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return found

def make_filename_id(filename):
  my_id = filename
  try:
    my_id = re.sub(".html$", "", my_id)
    my_id = re.sub("^group__", "", my_id)
    my_id = re.sub("__", "_", my_id)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return my_id

def fix_external_links(root, toc_data):
  try:
    matches = root.xpath(".//a[@href]")
    for match in matches:
      href = match.get("href")
      if re.match("^https?:", href) is None and re.match("^#", href) is None:
        filename = href
        target_id = None
        if "#" in href:
          filename = href.split("#")[0]
          target_id = href.split("#")[1]
        # walk the toc data to find the main html file
        found = False
        parent_file = None
        for item in toc_data:
          if item == filename:
            parent_file = item
            found = True
            break
          else:
            for k, v in toc_data[item].items():
              found = find_item_in_dict(k,v,filename)
              if found == True:
                parent_file = item
                break
            if found == True:
              break
        if parent_file is not None:
          parent_file_dest = re.sub("^group__", "", parent_file)
          new_href = parent_file_dest
          if filename != parent_file:
            if target_id is None:
              my_id = make_filename_id(filename)
              new_href = new_href + "#" + my_id
            else:
              new_href = new_href + "#" + target_id
          new_href = re.sub("__", "_", new_href)
          match.set("href", new_href)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root

def merge_lists(list_type, root):
  try:
    # merge contiguous lists that came from the same original parent
    matches = root.findall(".//"+list_type+"[@data-parent-id]")
    for match in matches:
      my_ref = match.get("data-parent-id")
      next_el = match.getnext()
      if next_el is not None:
        next_ref = next_el.get("data-parent-id")
      while next_el is not None and next_el.tag == list_type and next_ref is not None and next_ref == my_ref:
        for child in next_el.findall("./*"):
          match.append(child)
        next_el.getparent().remove(next_el)
        next_el = match.getnext()
        if next_el is not None:
          next_ref = next_el.get("data-parent-id")
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root

def wrap_list_items(root):
  try:
    matches = root.xpath(".//li[not(./p)]")
    for match in matches:
      newp = etree.Element("p")
      newp.text = match.text
      match.text = None
      for child in match.findall("./*"):
        newp.append(child)
      match.append(newp)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root

def make_cell_para(el):
  try:
    newp = etree.Element("p")
    newp.text = el.text
    el.text = None
    for child in el.findall("./*"):
      newp.append(child)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return newp

def merge_note_paras(root):
  try:
    matches = root.xpath(".//div[@class='admonitionblock note' and count(.//td[@class='content']) > 1]")
    for match in matches:
      first_cell = match.find(".//td[@class='content']")
      newp = make_cell_para(first_cell)
      first_cell.append(newp)
      next = first_cell.getnext()
      while next is not None:
        newp = make_cell_para(next)
        first_cell.append(newp)
        next.getparent().remove(next)
        next = first_cell.getnext()
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root

def fix_heading_levels(root):
  try:
    all_heads = root.xpath(".//p[contains(@class, 'adoc-h2')]|.//p[contains(@class, 'adoc-h3')]")
    if len(all_heads) > 0:
      head = all_heads[0]
      myclass = head.get("class")
      if "adoc-h3" in myclass:
        head.set("class", "adoc-h2")
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root

def get_document_title(root):
  title_text = ""
  try:
    title = root.find(".//div[@class='headertitle']/div[@class='title']")
    if title is not None:
      title_categories = title.find("./div[@class='ingroups']")
      if title_categories is not None:
        # move to the document contents
        contents = root.find(".//div[@class='contents']")
        if contents is not None:
          contents.insert(0, title_categories)
          title_categories.text = "Part of: " + title_categories.text if title_categories.text is not None else "Part of: "
      title_text = ''.join(get_all_text(title))
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return title_text

def retag_heading(head, headtype):
  try:
    text = ''.join(get_all_text(head))
    newel = etree.Element("p")
    newel.set("class", "adoc-"+headtype)
    anchors = head.xpath("./a[@class='anchor' and @id]")
    if len(anchors) > 0:
      anchor = anchors[0]
    else:
      anchor = None
    if anchor is not None and anchor.text is None:
      newel.set("id", anchor.get("id"))
    else:
      newel.set("id", head.get("id"))
    newel.text = text
    head.addnext(newel)
    head.getparent().remove(head)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return

def prep_for_adoc(root):
  try:
    h2s = root.xpath(".//div[@class='contents']/h2|.//div[@class='contents']/div[@class='textblock']/h2")
    for head in h2s:
      retag_heading(head, "h2")
    h3s = root.xpath(".//div[@class='contents']/h3|.//div[@class='contents']/div[@class='textblock']/h3")
    for head in h3s:
      retag_heading(head, "h3")
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root

def make_adoc(root_string, title_text, filename):
  try:
    my_id = make_filename_id(filename)
    root_string = re.sub("<\/div>\s*?$", "", root_string, flags=re.S)
    root_string = re.sub('<div class="contents" id="\S*?">', "", root_string)
    root_string = "[["+my_id+"]]\n== " + title_text + "\n\n++++\n" + root_string
    root_string = re.sub('(<p[^>]+class="adoc-h2"[^>]*id=")([^"]+)("[^>]*>\s*)(.*?)(<\/p>)', '\n++++\n\n[[\\2]]\n=== \\4\n\n++++\n', root_string, flags=re.S)
    root_string = re.sub('(<p[^>]+class="adoc-h3"[^>]*id=")([^"]+)("[^>]*>\s*)(.*?)(<\/p>)', '\n++++\n\n[[\\2]]\n==== \\4\n\n++++\n', root_string, flags=re.S)
    root_string = root_string + "\n++++\n"
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root_string

def make_dict_path(arr, level):
  try:
    dict_path_str = ""
    counter = level
    while counter >= 0:
      dict_path_str = "['"+arr[counter]+"']" + dict_path_str
      counter -= 1
    dict_path_str = "toc_data" + dict_path_str
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return dict_path_str

def parse_toc(root):
  try:
    toc_data = {}
    parents = []
    items = root.findall(".//a[@class='el']")
    for item in items:
      href = item.get("href")
      target = item.get("target")
      if target != "_self":
        continue
      parent = item.xpath("./ancestor::tr")[-1]
      parent_id = parent.get("id")
      level = len(parent_id.split("_"))-2
      parent_level = level-1
      if parent_level == 0:
        # just add it to the main tree
        toc_data[href] = {}
      else:
        # add it as a child at the correct nesting level
        cmd = make_dict_path(parents, parent_level-1)
        cmd = cmd + "[href] = {}"
        exec(cmd)
      if len(parents) > level-1:
        parents[level-1] = href
      else:
        parents.append(href)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return toc_data

def parse_header(header_path):
  h_json = {
    'index_doxygen': { 'name': 'Introduction', 'description': 'An introduction to the Pico SDK', 'subitems': [] }
  }
  try:
    with open(header_path) as h:
      content = h.read()
    blocks = re.findall("^(\s*)(\*|\/\*\*)(\s*)(\s)(\*)(\s)(\\\\)(defgroup)([^}]*)(\@\})", content, re.M)
    for (a, b, c, d, e, f, g, h, i, j) in blocks:
      items = i.split("\defgroup")
      group_id = None
      for item in items:
        if group_id is None: # must be the first item in the list
          m = re.match("(\s*)(\S*)(\s*)([^*]*)(.*?)(@\{)", item, re.S)
          group_id = m.group(2)
          group_filename = "group_"+group_id+".html"
          group_filename = re.sub("_", "__", group_filename)
          group_name = m.group(4)
          group_name = re.sub("\s*$", "", group_name, re.M)
          group_desc = m.group(5)
          group_desc = re.sub("\n", "", group_desc, re.M)
          group_desc = re.sub("\*", "", group_desc, re.M)
          group_desc = re.sub("^\s", "", group_desc, re.M)
          h_json[group_id] = { 'name': group_name, 'description': group_desc, 'filename': group_filename, 'subitems': [] }
        else:
          cleaned = item
          cleaned = re.sub("\n*", "", cleaned, re.M)
          cleaned = re.sub("^\s*", "", cleaned, re.M)
          cleaned = re.sub("\s*\*\s*$", "", cleaned, re.M)
          val = cleaned.split(" ")[0]
          filename = re.sub("_", "__", val)
          filename = "group__" + filename
          h_json[group_id]['subitems'].append({ 'name': val, 'file': filename + ".adoc" })
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return h_json

def compile_json_mappings(json_dir, json_files):
  try:
    compiled = []
    skip = ["table_memname.json"]
    for json_file in sorted(json_files):
      if json_file not in skip:
        # read the json
        file_path = os.path.join(json_dir, json_file)
        with open(file_path) as f:
          data = json.load(f)
        compiled.append(data)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return compiled

def walk_json(k,v,group_adoc):
  try:
    filename = re.sub("html$", "adoc", k)
    group_adoc = group_adoc + "include::" + filename + "[]\n\n"
    if len(v) > 0:
      for sk, sv in v.items():
        group_adoc = walk_json(sk,sv,group_adoc)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return group_adoc

def walk_nested_adoc(k, v, output_path, level):
  try:
    # only adjust nested items
    if level > 1:
      # read the adoc file
      adoc_path = re.sub(".html$", ".adoc", k)
      filepath = os.path.join(output_path, adoc_path)
      with open(filepath) as f:
        content = f.read()
      subs = "="
      for i in range(level-1):
        subs = subs + "="
      content = re.sub("^=", subs, content, flags=re.M)
      # print(content)
      write_output(filepath, content)
      # adjust the heading levels
    for sk,sv in v.items():
      newlevel = level + 1
      newlevel = walk_nested_adoc(sk, sv, output_path, newlevel)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return level

def handler(html_path, output_path, header_path, output_json):
  try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_dir = os.path.join(dir_path, "doxygen_json_mappings")
    html_dir = os.path.realpath(html_path)
    output_dir = os.path.realpath(output_path)
    # get the file order and groupings
    h_json = parse_header(header_path)
    toc_data = None
    # read the json transform mappings:
    # get all the json files within a specified directory
    json_files = os.listdir(json_dir)
    # filter for just json files
    json_files = [f for f in json_files if re.search(".json", f) is not None]
    complete_json_mappings = compile_json_mappings(json_dir, json_files)
    # get a list of all the html files
    html_files = os.listdir(html_dir)
    html_files = [f for f in html_files if re.search(".html", f) is not None]
    # sort the files ascending
    html_files.sort()
    # get the TOC data
    toc_file = os.path.join(html_path, "modules.html")
    if os.path.exists(toc_file):
      with open(toc_file) as h:
        toc_root = etree.HTML(h.read())
      toc_data = parse_toc(toc_root)
    # process every html file
    updated_links = {}
    for html_file in html_files:
      # create the full path
      this_path = os.path.join(html_path, html_file)
      this_output_path = os.path.join(output_path, html_file)
      # read the input root
      with open(this_path) as h:
        html_content = h.read()
        html_content = re.sub('<\!DOCTYPE html PUBLIC "-\/\/W3C\/\/DTD XHTML 1\.0 Transitional\/\/EN" "https:\/\/www\.w3\.org\/TR\/xhtml1\/DTD\/xhtml1-transitional\.dtd">', '', html_content)
        html_content = re.sub('rel="stylesheet">', 'rel="stylesheet"/>', html_content)
        html_content = re.sub('&display=swap"', '"', html_content)
        html_content = re.sub('<img src="logo-mobile\.svg" alt="Raspberry Pi">', '', html_content)
        html_content = re.sub('<img src="logo\.svg" alt="Raspberry Pi">', '', html_content)
        html_content = re.sub("<\!-- HTML header for doxygen \S*?-->", '', html_content)
        html_content = re.sub(' xmlns="http://www.w3.org/1999/xhtml"', '', html_content)
        root = etree.HTML(html_content)
      
      # give everything an id
      root = add_ids(root, html_file)
      # loop over each json file
      skip = ["table_memname.json"]
      for mapping in complete_json_mappings:
        for item in mapping:
          root = transform_element(item, root)
      # fix links
      root, updated_links = fix_internal_links(root, html_file, updated_links)
      root = fix_external_links(root, toc_data)
      # cleanup
      root = merge_lists("ul", root)
      root = merge_lists("ol", root)
      root = wrap_list_items(root)
      # combine multi-para notes into one container
      root = merge_note_paras(root)
      # add some extra items to help with the adoc conversion
      root = prep_for_adoc(root)
      # fix some heading levels
      root = fix_heading_levels(root)
      root = fix_duplicate_ids(root, html_file)
      # cleanup
      root = strip_attribute("data-processed", root)
      # get the document title
      title_text = get_document_title(root)
      # get only the relevant content
      contents = root.find(".//div[@class='contents']")
      # prep and write the adoc
      final_output = stringify(contents)
      adoc = make_adoc(final_output, title_text, html_file)
      adoc_path = re.sub(".html$", ".adoc", this_output_path)
      write_output(adoc_path, adoc)
      print("Generated " + adoc_path)

    # adjust nested adoc headings
    for k,v in toc_data.items():
      level = 0
      # walk the tree and adjust as necessary
      level = walk_nested_adoc(k, v, output_path, level)

    # fix any links that were updated from other files
    adoc_files = os.listdir(output_path)
    adoc_files = [f for f in adoc_files if re.search(".adoc", f) is not None]
    for adoc_file in adoc_files:
      this_path = os.path.join(output_path, adoc_file)
      with open(this_path) as h:
        content = h.read()
      for link in updated_links:
        content = re.sub(link, updated_links[link], content)
      write_output(this_path, content)
    
    # make the group adoc files
    # include::micropython/what-board.adoc[]
    for item in h_json:
      group_adoc = "= " + h_json[item]['name'] + "\n\n"
      group_adoc = group_adoc + h_json[item]['description'] + "\n\n"
      if 'filename' in h_json[item]:
        item_filename = h_json[item]['filename']
        for k,v in toc_data[item_filename].items():
          group_adoc = walk_json(k,v,group_adoc)
      group_output_path = os.path.join(output_path, item + ".adoc")
      write_output(group_output_path, group_adoc)
    # write the json structure file as well
    write_output(output_json, json.dumps(h_json, indent="\t"))
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return

if __name__ == "__main__":
  html_path = sys.argv[1]
  output_path = sys.argv[2]
  header_path = sys.argv[3]
  output_json = sys.argv[4]
  handler(html_path, output_path, header_path, output_json)
