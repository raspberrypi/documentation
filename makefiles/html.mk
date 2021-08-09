# This Makefile "makes" the documentation/html directory, i.e. converts asciidoc to html

include makefiles/shared.mk

OUTPUT_DIR = $(HTML_DIR)
REQUIRED_MARKER_FILE = $(ASCIIDOC_BUILD_DIR)/.done
MARKER_FILE = $(OUTPUT_DIR)/.done

# The $(MARKER_FILE) could be used as a prereq for other post-processing rules
all: | $(MARKER_FILE)

clean:
	rm -rf $(OUTPUT_DIR)
	rm -rf .sass-cache

# Some of the source-files have changed, so things might need to be rebuilt
invalidate:
	rm -f $(MARKER_FILE)

.PHONY: all clean invalidate serve

$(MARKER_FILE): | $(REQUIRED_MARKER_FILE)
	$(JEKYLL) build
	touch $@

# this is very similar to the previous rule, but this rule doesn't create $(MARKER_FILE) because
# the feed.xml created by `jekyll serve` is different to `jekyll build`
serve: | $(REQUIRED_MARKER_FILE)
	$(JEKYLL) serve
