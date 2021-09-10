# This Makefile contains rules for making the documentation/html directory, i.e. converts asciidoc to html

# The $(HTML_MARKER_FILE) could be used as a prereq for other post-processing rules
html: | $(HTML_MARKER_FILE)

clean_html:
	rm -rf $(HTML_DIR)

# Some of the source-files have changed, so things might need to be rebuilt
invalidate_html:
	rm -f $(HTML_MARKER_FILE)

.PHONY: html clean_html invalidate_html serve_html

$(HTML_MARKER_FILE): | $(JEKYLL_MARKER_FILE)
	$(JEKYLL) build
	touch $@

# this is very similar to the previous rule, but this rule doesn't create $(JEKYLL_MARKER_FILE) because
# the feed.xml created by `jekyll serve` is different to `jekyll build`
serve_html: | $(JEKYLL_MARKER_FILE)
	$(JEKYLL) serve
