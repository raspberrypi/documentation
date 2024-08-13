#!/usr/bin/env python3

import os
import re
import subprocess
import shutil
import unittest
import json
import datetime

# to run: on the command line, run all scripts from the top dir: pytest,
# or: python3 -m unittest tests.test_create_nav

# NOTE: This test is unfortunately not standalone -- it requires 
# that you've run both make build_doxygen_adoc and make first.

class TestCreateNav(unittest.TestCase):
    def setUp(self):
        script_path = os.path.realpath(__file__)
        self.top_dir = re.sub(r"/tests/[^/]+$", "", script_path)
        self.fixtures_path = os.path.join(self.top_dir, "tests", "fixtures")
        self.script_path = os.path.join(self.top_dir, "scripts")
        self.process_path = os.path.join(self.script_path, "create_nav.py")
        self.build_path = os.path.join(self.fixtures_path, "build")
        self.output_path = os.path.join(self.build_path, "jekyll", "_data")
        self.output_file = os.path.join(self.output_path, "nav.json")

    def tearDown(self):
        shutil.rmtree(self.build_path)

    def test_create_nav(self):
        os.makedirs(self.output_path)
        index_json = os.path.join(self.fixtures_path, "build_jekyll_data_index.json")
        adoc_dir = os.path.join(self.fixtures_path)
        output_json = self.output_file

        subprocess.run(["python3", self.process_path, index_json, adoc_dir, output_json])
        expected = r'''[
    {
        "title": "Microcontrollers",
        "path": "/microcontrollers/",
        "toc": [
            {
                "path": "/microcontrollers/c_sdk.html",
                "title": "The C/C++ SDK",
                "sections": [
                    {
                        "heading": "SDK Setup",
                        "anchor": "sdk-setup"
                    },
                    {
                        "heading": "Raspberry Pi Pico C/{cpp} SDK",
                        "anchor": "raspberry-pi-pico-ccpp-sdk"
                    },
                    {
                        "heading": "Your First Binaries",
                        "anchor": "your-first-binaries",
                        "subsections": [
                            {
                                "heading": "Blink an LED",
                                "anchor": "blink-an-led"
                            },
                            {
                                "heading": "Say \"Hello World\"",
                                "anchor": "say-hello-world"
                            }
                        ]
                    },
                    {
                        "heading": "Quick-start your own project",
                        "anchor": "quick-start-your-own-project"
                    }
                ]
            }
        ]
    }
]'''
        res = ""
        if os.path.isfile(self.output_file):
            with open(self.output_file) as f:
                res = f.read()
        self.assertTrue(expected == res)

def run_create_nav_tests(event, context):
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCreateNav)
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
