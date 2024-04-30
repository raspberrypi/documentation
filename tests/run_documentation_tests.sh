#! /bin/bash

# run from the top level: ./tests/run_documentation_tests.sh

python3 -m unittest tests.test_create_build_adoc_doxygen
python3 -m unittest tests.test_create_build_adoc_include
python3 -m unittest tests.test_create_build_adoc
python3 -m unittest tests.test_create_nav
cd scripts/
python3 -m unittest tests.test_doxygen_adoc
