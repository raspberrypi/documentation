import os 
import re
import unittest
from pathlib import Path
from transform_doxygen_html import parse_individual_file
from transform_doxygen_html import compile_json_mappings

# to run: on the command line, from the /scripts dir: python3 -m unittest tests.test_doxygen_adoc

class TestDoxygenAdoc(unittest.TestCase):
	def setUp(self):
		self.current_file = os.path.realpath(__file__)
		self.current_dir = Path(self.current_file).parent.absolute()
		self.parent_dir = re.sub("/tests", "", str(self.current_dir))

	def tearDown(self):
		pass

	def test_parse_individual_file(self):
		updated_links = {}
		html_path = os.path.join(self.current_dir, "fixtures")
		adoc_fixture = os.path.join(html_path, "expected_adoc.adoc")
		html_file = "group__hardware__dma.html"
		json_dir = os.path.join(self.parent_dir, "doxygen_json_mappings")
		json_files = os.listdir(json_dir)
		json_files = [f for f in json_files if re.search(".json", f) is not None]
		complete_json_mappings = compile_json_mappings(json_dir, json_files)
		h_json = [{'group_id': 'hardware', 'name': 'Hardware APIs', 'description': 'This group of libraries provides a thin and efficient C API / abstractions to access the RP2040 hardware without having to read and write  hardware registers directly.  ', 'html': 'group__hardware.html', 'subitems': [{'name': 'hardware_dma', 'file': 'group__hardware__dma.adoc', 'html': 'group__hardware__dma.html', 'subitems': []}]}]
		adoc, h_json = parse_individual_file(html_path, html_file, complete_json_mappings, updated_links, h_json)
		adoc_cleaned = re.sub("rpip[a-zA-Z0-9]+", "", adoc)
		expected_json = [{'group_id': 'hardware', 'name': 'Hardware APIs', 'description': 'This group of libraries provides a thin and efficient C API / abstractions to access the RP2040 hardware without having to read and write  hardware registers directly.  ', 'html': 'group__hardware.html', 'subitems': [{'name': 'hardware_dma', 'file': 'group__hardware__dma.adoc', 'html': 'group__hardware__dma.html', 'subitems': [{'name': 'group__channel__config', 'file': 'group__channel__config.adoc', 'html': 'group__channel__config.html', 'subitems': []}]}]}]
		with open(adoc_fixture) as f:
			expected_adoc = f.read()
		expected_adoc_cleaned = re.sub("rpip[a-zA-Z0-9]+", "", expected_adoc)
		self.assertEqual(expected_json, h_json)
		self.assertEqual(expected_adoc_cleaned, adoc_cleaned)

	def test_doxygen_adoc_variables(self):
		# run AFTER the content has been built;
		# test will fail if ANY of the below are different or missing
		expected = {
			"pico-sdk/index_doxygen.adoc" : [
				":doctitle: Raspberry Pi Documentation - Introduction",
				":page-sub_title: Introduction"
			],
			"pico-sdk/hardware.adoc": [
				":doctitle: Raspberry Pi Documentation - Hardware APIs",
				":page-sub_title: Hardware APIs"
			],
			"pico-sdk/high_level.adoc": [
				":doctitle: Raspberry Pi Documentation - High Level APIs",
				":page-sub_title: High Level APIs"
			],
			"pico-sdk/third_party.adoc": [
				":doctitle: Raspberry Pi Documentation - Third-party Libraries",
				":page-sub_title: Third-party Libraries"
			],
			"pico-sdk/networking.adoc": [
				":doctitle: Raspberry Pi Documentation - Networking Libraries",
				":page-sub_title: Networking Libraries"
			],
			"pico-sdk/runtime.adoc": [
				":doctitle: Raspberry Pi Documentation - Runtime Infrastructure",
				":page-sub_title: Runtime Infrastructure"
			],
			"pico-sdk/misc.adoc": [
				":doctitle: Raspberry Pi Documentation - External API Headers",
				":page-sub_title: External API Headers"
			]
		}

		# get the appropriate working dir
		file_path = os.path.join(self.parent_dir, "..", "build", "jekyll")

		for item in expected:
			print("FILE: ", item)
			# find the file
			this_path = os.path.join(file_path, item)
			# make sure the file exists
			if os.path.isfile(this_path):
				# open the file and read the content
				with open(this_path) as f:
					content = f.read()
				# find each expected line
				for line in expected[item]:
					print("LOOKING FOR: ", line)
					match = re.search(line, content, re.M)
					self.assertTrue(match is not None)
			else:
				print("Could not find this file. did you run `make` first?")

def run_doxygen_adoc_tests(event, context):
	suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestDoxygenAdoc)
	result = unittest.TextTestRunner(verbosity=2).run(suite)
	if result.wasSuccessful():
		body = { "message": "Tests passed!" }
		response = {
			"statusCode": 200,
			"body": json.dumps(body)
		}
		return response
	else  :
		body = { "message": "Tests failed!" }
		response = {
			"statusCode": 500,
			"body": json.dumps(body)
		}
		return response

if __name__ == '__main__':
	unittest.main()
