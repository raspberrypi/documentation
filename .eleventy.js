module.exports = function(eleventyConfig) {
  // Located in ./_content/_includes/layouts/default.html
  eleventyConfig.addLayoutAlias('default', 'layouts/default.html');

  return {
    dir: {
      input: ".",
      output: "./_site",
    }
  };
};
