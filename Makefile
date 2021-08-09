# The top-level Makefile which does things by calling rules in other makefiles

# these need to be done in a specific order, which is why they're rules rather than simply being listed as prerequisites
all:
	$(MAKE) jekyll
	$(MAKE) html

clean:
	$(MAKE) clean_html
	$(MAKE) clean_jekyll
	rm -rf build

.PHONY: all clean jekyll clean_jekyll invalidate_jekyll update_offline_includes html clean_html invalidate_html serve_html

# Copy all needed files to the build/jekyll folder
jekyll:
	$(MAKE) -f makefiles/jekyll.mk all

# Delete the build/jekyll directory
clean_jekyll:
	$(MAKE) -f makefiles/jekyll.mk clean

# Tell the build/jekyll directory that some of its source-files might have changed
invalidate_jekyll:
	$(MAKE) -f makefiles/jekyll.mk invalidate

# Update the files in the offline_includes directory
update_offline_includes:
	$(MAKE) -f makefiles/jekyll.mk $@

# Convert asciidoc files to html files
html:
	$(MAKE) -f makefiles/html.mk all

# Delete the documentation/html directory
clean_html:
	$(MAKE) -f makefiles/html.mk clean

# Tell the documentation/html directory that some of its source-files might have changed
invalidate_html:
	$(MAKE) -f makefiles/html.mk invalidate

# Serve the html directory with Jekyll
serve_html:
	$(MAKE) -f makefiles/html.mk serve

