#!/usr/bin/env python3

import os
import sys
import json
import re

def get_release_version(doxyfile_path):
	version = "unknown"
	with open(doxyfile_path) as f:
		doxy_content = f.read()
	version_search = re.search("(\nPROJECT_NUMBER\s*=\s*)([\d.]+)", doxy_content)
	if version_search is not None:
		version = version_search.group(2)
	return version

def write_new_data_file(output_json_file, data_obj):
	f = open(output_json_file, 'w')
	f.write(json.dumps(data_obj))
	f.close()

if __name__ == "__main__":
	# read the doxygen config file
	doxyfile_path = sys.argv[1]
	# output the new data file
	output_json_file = sys.argv[2]
	version = get_release_version(doxyfile_path)
	data_obj = {"pico_sdk_release": version}
	write_new_data_file(output_json_file, data_obj)
