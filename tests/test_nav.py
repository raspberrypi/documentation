import os 
import re
import unittest
import json
from pathlib import Path

# to run: on the command line, from the top level: python3 -m unittest tests.test_nav

class TestNav(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass			

	def test_nav_contents(self):
		current_file = os.path.realpath(__file__)
		current_dir = Path(current_file).parent.absolute()
		parent_dir = re.sub("/tests", "", str(current_dir))
		nav_fixture = os.path.join(current_dir, "fixtures", "nav.json")
		nav_path = os.path.join(parent_dir, "build", "jekyll", "_data", "nav.json")
		# read the fixture file
		with open(nav_fixture) as f:
			nav_base_data = f.read()
		# read the new file
		with open(nav_path) as f:
			nav_new_data = f.read()
		self.assertEqual(nav_base_data, nav_new_data)

def run_nav_tests(event, context):
	suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestNav)
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
