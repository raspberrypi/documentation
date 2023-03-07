#!/usr/bin/env python3

import os
import sys
import json
import re

def add_release_version(doxyfile_path, data_obj):
	with open(doxyfile_path) as f:
		doxy_content = f.read()
	version_search = re.search("(\nPROJECT_NUMBER\s*=\s*)([\d.]+)", doxy_content)
	if version_search is not None:
		version = version_search.group(2)
		data_obj["pico_sdk_release"] = version
	return data_obj

def write_new_data_file(output_dir, data_obj):
	f = open(output_dir, 'w')
	f.write(json.dumps(data_obj))
	f.close()
	return

if __name__ == "__main__":
	# read the doxygen config file
	input_file = sys.argv[1]
	# output the new data file
	output_dir = sys.argv[2]
	data_obj = {}
	data_obj = add_release_version(input_file, data_obj)
	write_new_data_file(output_dir, data_obj)