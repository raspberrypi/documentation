# A bunch of common variables and rules shared by all the makefiles

include makefiles/shared_vars.txt

ASCIIDOC_BUILD_DIR = $(BUILD_DIR)/jekyll

$(BUILD_DIR):
	@mkdir -p $@
