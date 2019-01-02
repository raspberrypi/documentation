module.exports = function(eleventyConfig) {
  // Located in ./_content/_includes/layouts/default.html
  eleventyConfig.addLayoutAlias('default', 'layouts/default.html');

  // some Markdown contains links to [foo](bar.md) in order for hrefs in GitHub's UI to work correctly
  // however `.md` extensions need stripping from the output HTML...
  eleventyConfig.addTransform('stripMDExtension', function(content, outputPath) {
    if (outputPath.endsWith('.html')) {
      // handles links with a hash eg. "foo.md#bar"
      let stripMDExtensionsRetainHash = content.replace(/(.md)?(#.*)">/g, '$2">');
      // handles all remaining "foo.md"
      let stripMDExtensions = stripMDExtensionsRetainHash.replace(/(.md">)/g, '">');
      return stripMDExtensions;
    }
    return content;
  });

  return {
    dir: {
      input: ".",
      output: "./_site",
    }
  };
};
