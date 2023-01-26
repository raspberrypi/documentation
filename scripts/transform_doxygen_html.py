import json
import os
import sys
import re
import random
import string
import copy
import lxml
import lxml.html

try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # normal cElementTree install
    import cElementTree as etree
    print("running with cElementTree")
  except ImportError:
    try:
      # normal ElementTree install
      import elementtree.ElementTree as etree
      print("running with ElementTree")
    except ImportError:
      print("Failed to import ElementTree from any known place")

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

def stringify(root):
  html_string = etree.tostring(root, pretty_print=True, encoding='UTF-8').decode('utf-8')
  return html_string

def write_output(filepath, content):
  f = open(filepath, 'w')
  f.write(content)
  f.close()
  return

def add_ids(root):
  els = root.xpath(".//*[not(@id)]")
  for el in els:
    newid = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
    newid = "p" + newid
    el.set("id", newid)
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
    for child in match.iterchildren():
      target.append(child)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return new_tree

def transform_element(item, root, is_child=False):
  try:
    # build the selector for the xpath
    sel = make_selector(item["input"], is_child)
    print(sel)
    if sel is not None:
      matches = root.xpath(sel)
      print(matches)
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
          # then remove the element
          match.getparent().remove(match)
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
        for child in next_el.iterchildren():
          match.append(child)
        next_el.getparent().remove(next_el)
        next_el = match.getnext()
        if next_el is not None:
          next_ref = next_el.get("data-parent-id")
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

def prep_for_adoc(root):
  try:
    h2s = root.findall(".//div[@class='contents']/h2")
    print(h2s)
    for head in h2s:
      text = ''.join(get_all_text(head))
      newel = etree.Element("p")
      newel.set("class", "adoc-h2")
      newel.text = text
      head.addnext(newel)
      head.getparent().remove(head)
    h3s = root.findall(".//div[@class='contents']/h3")
    for head in h3s:
      text = ''.join(get_all_text(head))
      newel = etree.Element("p")
      newel.set("class", "adoc-h2")
      newel.text = text
      head.addnext(newel)
      head.getparent().remove(head)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root

def make_adoc(root_string, title_text):
  try:
    root_string = "= " + title_text + "\n\n++++\n" + root_string
    root_string = re.sub('(<p class="adoc-h2">\s*)(.*?)(\s*)(</p>)', '\n++++\n\n== \\2\n\n++++\n', root_string)
    root_string = re.sub('(<p class="adoc-h3">\s*)(.*?)(\s*)(</p>)', '\n++++\n\n=== \\2\n\n++++\n', root_string)
    root_string = root_string + "\n++++\n"
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return root_string

def handler(html_path, output_path):
  try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_dir = os.path.join(dir_path, "doxygen_json_mappings")
    html_dir = os.path.realpath(html_path)
    output_dir = os.path.realpath(output_path)
    # get a list of all the html files
    html_files = os.listdir(html_dir)
    html_files = [f for f in html_files if re.search(".html", f) is not None]
    # first, make sure the output dir exists
    # if os.path.isdir(output_dir) == False:
    #   os.mkdir(output_dir)
    # process every html file
    for html_file in html_files:
      # create the full path
      this_path = os.path.join(html_path, html_file)
      this_output_path = os.path.join(output_path, html_file)
      # read the input root
      with open(this_path) as h:
        root = etree.HTML(h.read())
      # give everything an id
      root = add_ids(root)
      # read the mappings:
      # get all the json files within a specified directory
      json_files = os.listdir(json_dir)
      # filter for just json files
      json_files = [f for f in json_files if re.search(".json", f) is not None]
      # loop over each json file
      skip = ["table_memname.json"]
      for json_file in json_files:
        if json_file not in skip:
          # read the json
          file_path = os.path.join(json_dir, json_file)
          with open(file_path) as f:
            data = json.load(f)
          # convert every element listed in the json file
          for item in data:
            root = transform_element(item, root)
      # cleanup
      root = merge_lists("ul", root)
      root = merge_lists("ol", root)
      # add some extra items to help with the adoc conversion
      root = prep_for_adoc(root)
      # get the document title
      title_text = get_document_title(root)
      # get only the relevant content
      contents = root.find(".//div[@class='contents']")
      # prep and print the processed html
      final_output = ""
      for child in contents.iterchildren():
        final_output = final_output + "\n" + stringify(child)
      # prep and write the adoc
      adoc = make_adoc(final_output, title_text)
      adoc_path = re.sub(".html$", ".adoc", this_output_path)
      write_output(adoc_path, adoc)
      # output_path = os.path.join(html_dir, "out.html")
      # write_output(this_output_path, final_output)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("ERROR: ", e, exc_tb.tb_lineno)
  return

if __name__ == "__main__":
  html_path = sys.argv[1]
  output_path = sys.argv[2]
  handler(html_path, output_path)