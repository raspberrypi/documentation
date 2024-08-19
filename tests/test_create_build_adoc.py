#!/usr/bin/env python3

import os
import re
import subprocess
import shutil
import unittest
import json
import datetime

# to run: on the command line, run all scripts from the top dir: pytest,
# or: python3 -m unittest tests.test_create_build_adoc

class TestCreateBuildAdoc(unittest.TestCase):
    def setUp(self):
        script_path = os.path.realpath(__file__)
        top_dir = re.sub(r"/tests/[^/]+$", "", script_path)
        self.fixtures_path = os.path.join(top_dir, "tests", "fixtures")
        self.script_path = os.path.join(top_dir, "scripts")
        self.process_path = os.path.join(self.script_path, "create_build_adoc.py")
        self.build_path = os.path.join(self.fixtures_path, "build")
        self.output_path = os.path.join(self.build_path, "jekyll", "microcontrollers")
        self.output_file = os.path.join(self.output_path, "c_sdk.adoc")

    def tearDown(self):
        shutil.rmtree(self.build_path)

    def test_create_build_adoc(self):
        os.makedirs(self.output_path)
        index_json = os.path.join(self.fixtures_path, "index.json")
        config_yaml = os.path.join(self.fixtures_path, "_config.yml")
        github_edit = os.path.join(self.fixtures_path, "github_edit.adoc")
        src_adoc = os.path.join(self.fixtures_path, "microcontrollers", "c_sdk.adoc")
        includes_dir = os.path.join(self.fixtures_path, "build", "adoc_includes")
        build_adoc = self.output_file

        subprocess.run(["python3", self.process_path, index_json, config_yaml, github_edit, src_adoc, includes_dir, build_adoc])
        expected = ''':parentdir: microcontrollers
:page-layout: docs
:includedir: {0}
:doctitle: The C/C++ SDK - Raspberry Pi Documentation
:page-sub_title: The C/C++ SDK
:sectanchors:
:figure-caption!:
:source-highlighter: rouge

include::{{includedir}}/{{parentdir}}/c_sdk/sdk_setup.adoc[]

include::{{includedir}}/{{parentdir}}/c_sdk/official_sdk.adoc[]

include::{{includedir}}/{{parentdir}}/c_sdk/your_first_binary.adoc[]

include::{{includedir}}/{{parentdir}}/c_sdk/quick_start.adoc[]
'''.format(os.path.join(self.build_path, "adoc_includes"))
        res = ""
        if os.path.isfile(self.output_file):
            with open(self.output_file) as f:
                res = f.read()
        self.assertTrue(expected == res)

def run_create_build_adoc_tests(event, context):
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCreateBuildAdoc)
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
