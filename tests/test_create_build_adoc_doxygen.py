#!/usr/bin/env python3

import os
import re
import subprocess
import shutil
import unittest
import json
import datetime

# 503 281 1142

# to run: on the command line, run all scripts from the top dir: pytest,
# or: python3 -m unittest tests.test_create_build_adoc_doxygen

class TestCreateBuildAdocDoxygen(unittest.TestCase):
    def setUp(self):
        script_path = os.path.realpath(__file__)
        top_dir = re.sub(r"/tests/[^/]+$", "", script_path)
        self.fixtures_path = os.path.join(top_dir, "tests", "fixtures")
        self.script_path = os.path.join(top_dir, "scripts")
        self.process_path = os.path.join(self.script_path, "create_build_adoc_doxygen.py")
        self.build_path = os.path.join(self.fixtures_path, "build")
        self.output_path = os.path.join(self.build_path, "jekyll", "pico-sdk")
        self.output_file = os.path.join(self.output_path, "group__channel__config.adoc")

    def tearDown(self):
        shutil.rmtree(self.build_path)

    def test_create_build_adoc_doxygen(self):
        os.makedirs(self.output_path)
        index_json = os.path.join(self.fixtures_path, "index.json")
        config_yaml = os.path.join(self.fixtures_path, "_config.yml")
        src_adoc = os.path.join(self.fixtures_path, "pico-sdk", "group__channel__config.adoc")
        picosdk_json = os.path.join(self.fixtures_path, "pico-sdk", "picosdk_index.json")
        includes_dir = os.path.join(self.fixtures_path, "build", "adoc_includes")
        build_adoc = self.output_file

        subprocess.run(["python3", self.process_path, index_json, config_yaml, src_adoc, picosdk_json, includes_dir, build_adoc])
        expected = ''':parentdir: pico-sdk
:page-layout: docs
:includedir: {0}
:doctitle: group__channel__config - Raspberry Pi Documentation
:page-sub_title: group__channel__config
:sectanchors:
:figure-caption!:
:source-highlighter: rouge

[[channel_config]]
== channel_config

++++


<div class="ingroups" id="rpipf87063354e1b844cb285">Part of: <a class="el" href="hardware.html" id="rpip7b15f314e61b3d67d47a">Hardware APIs</a> » <a class="el" href="hardware.html#hardware_dma" id="rpipff99d40da73fc6dea3fa">hardware_dma</a></div><p id="rpip53d2edb3499ae77e6177">DMA channel configuration   .  
<a href="#gaebee0ee46a0e8f91042d" id="rpipe8e703f5e5c1e27bc721" data-adjusted="true">More...</a></p>

++++

[[rpipbcecd949811e64d5957a]]
=== Functions


++++

<ul class="memberdecls" id="r_ga28d1103cea7f7d73406a2aee44bfebd9" data-parent-id="rpip9346572900aa9571ed1e"><li class="memitem"><p data-target="true" data-target-for="r_ga28d1103cea7f7d73406a2aee44bfebd9"><span class="memItemLeft" data-target="true" id="rpipba886656deedaa0dacb4" data-parent-id="r_ga28d1103cea7f7d73406a2aee44bfebd9" data-target-for="rpipba886656deedaa0dacb4">static void </span><span class="memItemRight" data-target="true" id="rpip5083c99dc8ed5710fa03" data-parent-id="r_ga28d1103cea7f7d73406a2aee44bfebd9" data-target-for="rpip5083c99dc8ed5710fa03"><a class="el" href="#ga28d1103cea7f7d73406a2aee44bfebd9" id="rpipe27a3a16c24ea1ffd583" data-adjusted="true">channel_config_set_read_increment</a> (<a class="el" href="structdma__channel__config.html" id="rpipd1a8408f6093cf231b71">dma_channel_config</a> *c, bool incr)</span></p>
</li></ul>
<a name="details" id="gaebee0ee46a0e8f91042d"/>
++++

[[rpip1326aa77c0728be36c25]]
=== Detailed Description


++++

<p id="rpipc21a40f920cc762d5fca">DMA channel configuration   . </p>
<p id="rpip461019a49239e7b74a04">A DMA channel needs to be configured, these functions provide handy helpers to set up configuration structures. See <a class="el" href="structdma__channel__config.html" id="rpip5392bc71bddfee8d94b2">dma_channel_config</a> </p>

++++

'''.format(os.path.join(self.fixtures_path, "build", "adoc_includes"))
        res = ""
        if os.path.isfile(self.output_file):
            with open(self.output_file) as f:
                res = f.read()
        self.assertTrue(expected == res)

def run_create_build_adoc_doxygen_tests(event, context):
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCreateBuildAdocDoxygen)
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
