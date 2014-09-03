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
  # copy files
  files = Dir.glob("*")
  mkdir BUILD_DIR
  cp_r files, BUILD_DIR

  # render markdown
  redcarpet = Redcarpet::Markdown.new Redcarpet::Render::HTML.new({}), {}

  md_files = Dir.glob File.join(BUILD_DIR, "**", "*.md")
  md_files.each do |md|
    html = redcarpet.render File.open(md).read
    File.open(md, File::WRONLY).write html
  end
  puts "Rendered #{md_files.length} markdown files."
end

desc "Remove the build"
task :clean do
  rm_rf BUILD_DIR
end

desc "Test the build"
task :test do
  HTML::Proofer.new(BUILD_DIR, { :ext => ".md", :directory_index_file => "README.md" }).run
end
