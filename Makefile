# The top-level Makefile which includes rules from other makefiles

include makefiles/shared_vars.txt

ASCIIDOC_BUILD_DIR = $(BUILD_DIR)/jekyll
JEKYLL_MARKER_FILE = $(ASCIIDOC_BUILD_DIR)/.done
HTML_MARKER_FILE = $(HTML_DIR)/.done

include makefiles/download_includes.mk
include makefiles/jekyll.mk
include makefiles/html.mk

.DEFAULT_GOAL := all

.PHONY: all clean

$(BUILD_DIR):
	@mkdir -p $@

all: | $(HTML_MARKER_FILE)

clean:
	rm -rf $(HTML_DIR)
	rm -rf $(BUILD_DIR)
