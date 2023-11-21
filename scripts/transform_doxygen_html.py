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

def find_item_in_toc(h_json, filename):
  try:
    found = False
    matching_file = None
    for item in h_json:
      if "html" in item and item["html"] == filename:
        matching_file = item["html"]
        found = True
        break
      elif "subitems" in item:
        matching_file, found = find_item_in_toc(item["subitems"], filename)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return matching_file, found

def fix_external_links(root, h_json):
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
        parent_file, found = find_item_in_toc(h_json, filename)
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

def get_document_title(root, html_file):
  title_text = re.sub(".html", "", html_file)
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

def decrease_heading_levels(adoc):
  try:
    adoc = re.sub("\n==", "\n=", adoc, flags=re.S)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return adoc

def traverse_subitems(subitems, toc_list):
  for item in subitems:
    if "html" in item:
      toc_list.append(item["html"])
    if "subitems" in item:
      toc_list = traverse_subitems(item["subitems"], toc_list)
  return toc_list

def parse_toc(h_json, toc_list):
  try:
    for item in h_json:
      if "filename" in item:
        toc_list.append(item["filename"])
      elif "subitems" in item:
        toc_list = traverse_subitems(item["subitems"], toc_list)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return h_json, toc_list

def parse_header(header_path):
  h_json = [
    { 'group_id': 'index_doxygen', 'name': 'Introduction', 'description': 'An introduction to the Pico SDK', 'html': 'index_doxygen.html', 'subitems': [] }
  ]
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
          group_json = { 'group_id': group_id, 'name': group_name, 'description': group_desc, 'html': group_filename, 'subitems': [] }
          h_json.append(group_json)
        else:
          cleaned = item
          cleaned = re.sub("\n*", "", cleaned, re.M)
          cleaned = re.sub("^\s*", "", cleaned, re.M)
          cleaned = re.sub("\s*\*\s*$", "", cleaned, re.M)
          val = cleaned.split(" ")[0]
          filename = re.sub("_", "__", val)
          filename = "group__" + filename
          group_json['subitems'].append({ 'name': val, 'file': filename + ".adoc", 'html': filename + ".html", 'subitems': [] })
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

def compile_includes(my_adoc, output_path, subitems):
  try:
    for item in subitems:
      # append includes directly to the parent file
      adoc_filename = item["file"]
      full_adoc_path = os.path.join(output_path, adoc_filename)
      # read the adoc
      included_content = ""
      with open(full_adoc_path) as f:
        included_content = f.read()
      my_adoc += "\n\n"
      my_adoc += included_content
      if "subitems" in item and len(item["subitems"]) > 0:
        my_adoc = compile_includes(my_adoc, output_path, item["subitems"])
      os.remove(full_adoc_path)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return my_adoc

def walk_json(item, group_adoc, output_path):
  try:
    filename = item["file"]
    group_adoc = group_adoc + "include::" + filename + "[]\n\n"
    if "subitems" in item and len(item["subitems"]) > 0:
      # compile includes into a single file
      my_adoc = ""
      my_adoc_path = os.path.join(output_path, filename)
      with open(my_adoc_path) as f:
        my_adoc = f.read()
      my_adoc = compile_includes(my_adoc, output_path, item["subitems"])
      # write the new file
      write_output(my_adoc_path, my_adoc)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return group_adoc

def walk_nested_adoc(item, output_path, level):
  try:
    # only adjust nested items
    if level > 1:
      # read the adoc file
      # not all items in the json have an adoc path
      adoc_path = re.sub(".html$", ".adoc", item["html"])
      filepath = os.path.join(output_path, adoc_path)
      with open(filepath) as f:
        content = f.read()
      subs = "="
      for i in range(level-1):
        subs = subs + "="
      content = re.sub("^=", subs, content, flags=re.M)
      write_output(filepath, content)
      # adjust the heading levels
    if "subitems" in item:
      for subitem in item["subitems"]:
        newlevel = level + 1
        newlevel = walk_nested_adoc(subitem, output_path, newlevel)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return level

# <div class="headertitle"><div class="title">timestamp<div class="ingroups"><a class="el" href="group__high__level.html">High Level APIs</a> &raquo; <a class="el" href="group__pico__time.html">pico_time</a></div></div></div>

# <table class="memberdecls">
# <tr class="heading"><td colspan="2"><h2 class="groupheader"><a id="groups" name="groups"></a>
# Modules</h2></td></tr>
# <tr class="memitem:group__sm__config" id="r_group__sm__config"><td class="memItemLeft" align="right" valign="top">&#160;</td><td class="memItemRight" valign="bottom"><a class="el" href="group__sm__config.html">sm_config</a></td></tr>
# <tr class="memdesc:group__sm__config"><td class="mdescLeft">&#160;</td><td class="mdescRight">PIO state machine configuration. <br /></td></tr>
# <tr class="separator:"><td class="memSeparator" colspan="2">&#160;</td></tr>
# <tr class="memitem:group__pio__instructions" id="r_group__pio__instructions"><td class="memItemLeft" align="right" valign="top">&#160;</td><td class="memItemRight" valign="bottom"><a class="el" href="group__pio__instructions.html">pio_instructions</a></td></tr>
# <tr class="memdesc:group__pio__instructions"><td class="mdescLeft">&#160;</td><td class="mdescRight">PIO instruction encoding. <br /></td></tr>
# <tr class="separator:"><td class="memSeparator" colspan="2">&#160;</td></tr>
# </table>

def find_toc_item(subitems, path, parent_tree):
  try:
    val = None
    original_tree = parent_tree.copy()
    for ix, item in enumerate(subitems):
      parent_tree.append(ix)
      if "html" in item and item["html"] == path:
        val = item
        break
      elif "subitems" in item:
        val, parent_tree = find_toc_item(item["subitems"], path, parent_tree)
      if val is None:
        parent_tree = original_tree.copy()
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return val, parent_tree

def check_toc_level(h_json, html_file, root):
  try:
    # check for the Modules table
    tables = root.xpath(".//table[@class='memberdecls' and ./tr/td/h2[contains(text(),'Modules')]]")
    if len(tables) > 0:
      table = tables[0]
      modules = table.xpath(".//tr[contains(@class, 'memitem:')]//a")
      modules = [f.get("href") for f in modules]
      # also collect this file's parents
      header = root.find(".//div[@class='headertitle']")
      outer_parents = []
      if header is not None:
        h_parents = header.findall(".//div[@class='ingroups']/a")
        for h_item in h_parents:
          outer_parents.append(h_item.get("href"))
      outer_parents.append(html_file)
      
      # first check the outer parents to find our starting point
      level = h_json
      for ix, parent in enumerate(outer_parents):
        #for toc_item in level:
        val, parent_tree = find_toc_item(level, parent, [])
        if val is not None:
          for n in parent_tree:
            level = level[n]
          if "subitems" not in level:
            level["subitems"] = []
          level = level["subitems"]
        # create each toc level as needed
        elif ix > 0:
          new_subitem = {'name': re.sub(".html", "", parent), 'file': re.sub(".html", ".adoc", parent), 'html': parent, 'subitems': []}
          level.append(new_subitem)
          level = new_subitem["subitems"]
      
      # then check all the modules
      for ix, module in enumerate(modules):
        found = False
        for toc_item in level:
          if "html" in toc_item and toc_item["html"] == module:
            found = True
            break
        if found == False:
          level.append({'name': re.sub(".html", "", module), 'file': re.sub(".html", ".adoc", module), 'html': module, 'subitems': []})
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return h_json

def parse_indiviual_file(html_path, html_file, complete_json_mappings, updated_links, h_json):
  try:
    # create the full path
    this_path = os.path.join(html_path, html_file)
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
    # first check to see if this should be in the toc list
    h_json = check_toc_level(h_json, html_file, root)
    # loop over each json file
    skip = ["table_memname.json"]
    for mapping in complete_json_mappings:
      for item in mapping:
        root = transform_element(item, root)
    # fix links
    root, updated_links = fix_internal_links(root, html_file, updated_links)
    root = fix_external_links(root, h_json)
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
    title_text = get_document_title(root, html_file)
    # get only the relevant content
    contents = root.find(".//div[@class='contents']")
    # prep and write the adoc
    final_output = stringify(contents)
    adoc = make_adoc(final_output, title_text, html_file)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return adoc, h_json

def handler(html_path, output_path, header_path, output_json):
  try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_dir = os.path.join(dir_path, "doxygen_json_mappings")
    html_dir = os.path.realpath(html_path)
    output_dir = os.path.realpath(output_path)
    # get the file order and groupings
    h_json = parse_header(header_path)
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
    # collect the TOC data
    # toc_file = os.path.join(html_path, "modules.html")
    # if os.path.exists(toc_file):
    #   with open(toc_file) as h:
    #     toc_root = etree.HTML(h.read())
    #   toc_data, toc_list = parse_toc(toc_root)
    # process every html file
    updated_links = {}

    for html_file in html_files:
      this_output_path = os.path.join(output_path, html_file)
      # parse the file
      adoc, h_json = parse_indiviual_file(html_path, html_file, complete_json_mappings, updated_links, h_json)
      # write the final adoc file
      adoc_path = re.sub(".html$", ".adoc", this_output_path)
      write_output(adoc_path, adoc)
      print("Generated " + adoc_path)

    toc_list = []
    toc_list = parse_toc(h_json, toc_list)

    # adjust nested adoc headings
    for item in h_json:
      level = 0
      # walk the tree and adjust as necessary
      level = walk_nested_adoc(item, output_path, level)

    # fix any links that were updated from other files
    adoc_files = os.listdir(output_path)
    adoc_files = [f for f in adoc_files if re.search(".adoc", f) is not None]
    for adoc_file in adoc_files:
      this_path = os.path.join(output_path, adoc_file)
      with open(this_path) as h:
        content = h.read()
      src_html_file = re.sub(".adoc", ".html", adoc_file)
      # fix heading levels for non-included pages
      if src_html_file not in toc_list:
        print(src_html_file)
        adoc = decrease_heading_levels(adoc)
      for link in updated_links:
        content = re.sub(link, updated_links[link], content)
      write_output(this_path, content)
    
    # make the group adoc files
    # include::micropython/what-board.adoc[]
    for item in h_json:
      group_adoc = "= " + item['name'] + "\n\n"
      group_adoc = group_adoc + item['description'] + "\n\n"
      if 'html' in item:
        item_filename = item['html']
        for toc_item in item["subitems"]:
          group_adoc = walk_json(toc_item,group_adoc,output_path)
      group_output_path = os.path.join(output_path, item["group_id"] + ".adoc")
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
