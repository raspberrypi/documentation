#!/usr/bin/env python3

import os
import re
import unittest
from pathlib import Path

# to run: on the command line, from the /scripts dir: python3 -m unittest tests.test_doxygen_adoc

class TestDoxygenAdoc(unittest.TestCase):
    def setUp(self):
        self.current_file = os.path.realpath(__file__)
        self.current_dir = Path(self.current_file).parent.absolute()
        self.parent_dir = re.sub("/tests", "", str(self.current_dir))

    def tearDown(self):
        pass

    def test_doxygen_adoc_variables(self):
        # run AFTER the content has been built;
        # test will fail if ANY of the below are different or missing
        expected = {
            "pico-sdk/index_doxygen.adoc" : [
                ":doctitle: Introduction - Raspberry Pi Documentation",
                ":page-sub_title: Introduction"
            ],
            "pico-sdk/hardware.adoc": [
                ":doctitle: Hardware APIs - Raspberry Pi Documentation",
                ":page-sub_title: Hardware APIs"
            ],
            "pico-sdk/high_level.adoc": [
                ":doctitle: High Level APIs - Raspberry Pi Documentation",
                ":page-sub_title: High Level APIs"
            ],
            "pico-sdk/third_party.adoc": [
                ":doctitle: Third-party Libraries - Raspberry Pi Documentation",
                ":page-sub_title: Third-party Libraries"
            ],
            "pico-sdk/networking.adoc": [
                ":doctitle: Networking Libraries - Raspberry Pi Documentation",
                ":page-sub_title: Networking Libraries"
            ],
            "pico-sdk/runtime.adoc": [
                ":doctitle: Runtime Infrastructure - Raspberry Pi Documentation",
                ":page-sub_title: Runtime Infrastructure"
            ],
            "pico-sdk/misc.adoc": [
                ":doctitle: External API Headers - Raspberry Pi Documentation",
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
