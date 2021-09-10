# This Makefile contains rules for downloading files to the build/jekyll/_inckudes directory

.PHONY: update_offline_includes

DOWNLOADED_INCLUDES = $(ASCIIDOC_BUILD_DIR)/_includes/header.html $(ASCIIDOC_BUILD_DIR)/_includes/fonts.html

offline_includes/tmp: offline_includes
	mkdir -p $@

offline_includes/tmp/%.html: $(SCRIPTS_DIR)/fetch_header_and_fonts.py | offline_includes/tmp
	OFFLINE_MODE=0 $< https://esi.raspberrypi.org/en/components/$*/ $@

# Update the files in the offline_includes directory
update_offline_includes: offline_includes/tmp/header.html offline_includes/tmp/fonts.html
	mv offline_includes/tmp/header.html offline_includes
	mv offline_includes/tmp/fonts.html offline_includes
	rmdir offline_includes/tmp

$(ASCIIDOC_BUILD_DIR)/_includes/%.html: $(SCRIPTS_DIR)/fetch_header_and_fonts.py | $(ASCIIDOC_BUILD_DIR)/_includes
	$< https://esi.raspberrypi.org/en/components/$*/ $@

$(JEKYLL_MARKER_FILE): $(DOWNLOADED_INCLUDES)
