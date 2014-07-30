require "rubygems"
require "rake"
require "redcarpet"
require "html/proofer"

BUILD_DIR = "./_build"

task :build => [:clean]
task :test => [:build]
task :default => [:test]

desc "Generate the build"
task :build do
  md_files = File.join "**", "*.md"
  Dir.glob(md_files) { |f|
    # input
    markdown = File.open(f).read
    html = Redcarpet::Markdown.new(
      Redcarpet::Render::HTML.new({}), {}
    ).render(markdown)

    # output
    dir = File.dirname File.join(BUILD_DIR, f)
    base = File.basename f
    FileUtils.mkdir_p dir
    File.open(File.join(dir, base), "w").write html
  }
end

desc "Remove the build"
task :clean do
  sh "rm -rf #{BUILD_DIR}"
end

desc "Test the"
task :test do
  HTML::Proofer.new(BUILD_DIR, { :ext => ".md" }).run
end
