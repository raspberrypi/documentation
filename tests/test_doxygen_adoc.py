import os 
import re
import unittest
from pathlib import Path

# to run: on the command line, from the top level: python3.9 -m unittest tests.test_pdf_visual_diff

class TestDoxygenAdoc(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass			

	def test_doxygen_adoc_variables(self):
		# run AFTER the content has been built;
		# test will fail if ANY of the below are different or missing
		expected = {
			"pico-sdk/index_doxygen.adoc" : [
				":doctitle: Raspberry Pi Documentation - index_doxygen",
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
		current_file = os.path.realpath(__file__)
		current_dir = Path(current_file).parent.absolute()
		parent_dir = re.sub("/tests", "", str(current_dir))
		print(parent_dir)
		file_path = os.path.join(parent_dir, "build", "jekyll")

		for item in expected:
			print("FILE: ", item)
			# find the file
			this_path = os.path.join(file_path, item)
			# open the file and read the content
			with open(this_path) as f:
				content = f.read()
			# find each expected line
			for line in expected[item]:
				print("LOOKING FOR: ", line)
				match = re.search(line, content, re.M)
				self.assertTrue(match is not None)

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
