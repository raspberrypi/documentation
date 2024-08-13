#!/usr/bin/env python3

import os
import re
import subprocess
import shutil
import unittest
import json
import datetime

# to run: on the command line, run all scripts from the top dir: pytest,
# or: python3 -m unittest tests.test_create_build_adoc_include

class TestCreateBuildAdocInclude(unittest.TestCase):
    def setUp(self):
        script_path = os.path.realpath(__file__)
        top_dir = re.sub(r"/tests/[^/]+$", "", script_path)
        self.fixtures_path = os.path.join(top_dir, "tests", "fixtures")
        self.script_path = os.path.join(top_dir, "scripts")
        self.process_path = os.path.join(self.script_path, "create_build_adoc_include.py")
        self.build_path = os.path.join(self.fixtures_path, "build")
        self.output_path = os.path.join(self.build_path, "jekyll", "microcontrollers", "csdk")
        self.output_file = os.path.join(self.output_path, "your_first_binary.adoc")

    def tearDown(self):
        shutil.rmtree(self.build_path)

    def test_create_build_adoc_include(self):
        os.makedirs(self.output_path)
        config_yaml = os.path.join(self.fixtures_path, "_config.yml")
        github_edit = os.path.join(self.fixtures_path, "github_edit.adoc")
        src_adoc = os.path.join(self.fixtures_path, "microcontrollers", "c_sdk", "your_first_binary.adoc")
        build_adoc = self.output_file

        subprocess.run(["python3", self.process_path, config_yaml, github_edit, src_adoc, build_adoc])
        expected = '''== Your First Binaries
[.edit-link]
Edit this {0}[on GitHub]



WARNING: If you are using an Apple Mac, and running macOS Ventura, there has been a change in how the Finder works which causes drag-and-drop to fail. Please see our https://www.raspberrypi.com/news/the-ventura-problem/[blog post] for a full explanation, and workarounds, and our https://github.com/raspberrypi/pico-sdk/issues/1081[Github issue] tracking the problem for the current status.

=== Blink an LED

The first program anyone writes when using a new microcontroller is to blink an LED on and off. The Raspberry Pi Pico comes with a single LED on-board. The LED is connected to `GP25` on the board's Raspberry Pi RP2040 for Pico, and `WL_GPIO0` on the Infineon 43439 wireless chip for Pico W.

image:images/Blink-an-LED-640x360-v2.gif[]

You can blink this on and off by,

. Download the Blink UF2 https://datasheets.raspberrypi.com/soft/blink.uf2[for Raspberry Pi Pico], or https://datasheets.raspberrypi.com/soft/blink_picow.uf2[for Pico W].
. Push and hold the BOOTSEL button and plug your Pico into the USB port of your Raspberry Pi or other computer.
. It will mount as a Mass Storage Device called RPI-RP2.
. Drag and drop the Blink UF2 binary onto the RPI-RP2 volume. Pico will reboot.

You should see the on-board LED blinking.

You can see the code on Github for the https://github.com/raspberrypi/pico-examples/blob/master/blink/blink.c[Raspberry Pi Pico] and https://github.com/raspberrypi/pico-examples/blob/master/pico_w/wifi/blink/picow_blink.c[Pico W] versions.

=== Say "Hello World"

The next program anyone writes is to say 'Hello World' over a USB serial connection.

image:images/Hello-World-640x360-v2.gif[]

. Download the https://datasheets.raspberrypi.com/soft/hello_world.uf2['Hello World' UF2].
. Push and hold the BOOTSEL button and plug your Pico into the USB port of your Raspberry Pi or other computer.
. It will mount as a Mass Storage Device called RPI-RP2.
. Drag and drop the 'Hello World' UF2 binary onto the RPI-RP2 volume. Pico will reboot.
. Open a Terminal window and type:
+
[source]
------
sudo apt install minicom
minicom -b 115200 -o -D /dev/ttyACM0
------

You should see 'Hello, world!' printed to the Terminal.

You can see the code https://github.com/raspberrypi/pico-examples/blob/master/hello_world/usb/hello_usb.c[on Github]
'''.format(os.path.join(self.fixtures_path, "microcontrollers", "c_sdk", "your_first_binary.adoc"))
        res = ""
        if os.path.isfile(self.output_file):
            with open(self.output_file) as f:
                res = f.read()
        self.assertTrue(expected == res)

def run_create_build_adoc_include_tests(event, context):
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCreateBuildAdocInclude)
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
