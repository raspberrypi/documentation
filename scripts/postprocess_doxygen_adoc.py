import re
import sys
import os
import json

# TO DO: fix links:
# collect all link anchors in the file
# then open each file, find all link, point to the correct anchor

def cleanup_text_page(adoc_file, output_adoc_path):
	script_path = os.path.realpath(__file__)
	top_dir_path = re.sub(r'/scripts/.*$', "", script_path)
	output_path = os.path.join(top_dir_path, adoc_file)
	with open(adoc_file) as f:
		adoc_content = f.read()
	# remove any errant spaces before anchors
	adoc_content = re.sub(r'( +)(\[\[[^[]*?\]\])', "\\2", adoc_content)
	with open(output_path, 'w') as f:
		f.write(adoc_content)
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

def postprocess_doxygen_adoc(adoc_file, output_adoc_path):
	sections = [{
		"group_id": "index_doxygen",
		"name": "Introduction",
		"description": "An introduction to the Pico SDK",
		"html": "index_doxygen.html",
		"subitems": []
	}]
	script_path = os.path.realpath(__file__)
	top_dir_path = re.sub(r'/scripts/.*$', "", script_path)
	output_path = os.path.join(top_dir_path, output_adoc_path)
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
	current_chapter = None
	chapter_dict = {}
	counter = 0
	for line in adoc_content.split('\n'):
		m = CHAPTER_START_RE.match(line)
		if m is not None:
			# write the previous chapter
			if current_chapter is not None:
				with open(chapter_filename, 'w') as f:
					f.write('\n'.join(current_chapter))
			# start the new chapter
			current_chapter = []
			# set the data for this chapter
			group_id = re.sub("^group_+", "", m.group(2))
			chapter_filename = os.path.join(output_path, group_id+".adoc")
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
		with open(chapter_filename, 'w') as f:
			f.write('\n'.join(current_chapter))
	build_json(sections, output_path)
	os.remove(adoc_file)
	return

if __name__ == '__main__':
	adoc_file = sys.argv[1]
	output_adoc_path = sys.argv[2]
	if re.search("all_groups.adoc", adoc_file) is not None:
		postprocess_doxygen_adoc(adoc_file, output_adoc_path)
	else:
		cleanup_text_page(adoc_file, output_adoc_path)
