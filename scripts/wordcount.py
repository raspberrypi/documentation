#!/usr/bin/env python3

from pathlib import Path
from bs4 import BeautifulSoup
import argparse
import sys

HTML_DIR = '../documentation/html'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default=HTML_DIR)
    args = parser.parse_args()
    print(args)

    directory = args.dir

    total_wordcount = 0

    # Get all HTML files in this directory
    html_files = list(Path(directory).rglob('*.html'))
    print("Number of articles: " + str(len(html_files)))

    if len(html_files) == 0:
        print("No HTML files in this directory. Ensure that you've recently built the docs and that you are providing the correct file path (relative or absolute) to the documentation/html directory with the --dir parameter.")
        sys.exit(1)

    for file in html_files:
        html = open(file).read()

        # Get just the stuff inside id="content" element
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find(id='content')
        # Count the words in that section
        if element:
            text = element.get_text()
            wordcount = len(text.split())
            # print(str(file) + " has " + str(wordcount) + " words in it")
            total_wordcount = total_wordcount + wordcount

    print("Number of words: " + str(total_wordcount))









