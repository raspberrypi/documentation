require "rubygems"
require "rake"
require "redcarpet"
require "html-proofer"

BUILD_DIR = "./_build"

task :build => [:clean]
task :test => [:build]
task :default => [:test]
task :html => [:build]

desc "change markdown files to html files for website deploy"
task :html do
  #get markdown files in BUILD_DIR
  md_files = Dir.glob File.join(BUILD_DIR,"**","*.md")
  md_files.each do |md|
    html = md.clone
    if html.include?("README.md")
      html["README.md"]="index.html"
    else 
      html[".md"] = ".html"
    end
    File.rename(md,html)
  end
end

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
  options = {
              :extension => ".md",
              :directory_index_file => "README.md"
            }
  HTMLProofer.check_directory(BUILD_DIR, options).run
end
