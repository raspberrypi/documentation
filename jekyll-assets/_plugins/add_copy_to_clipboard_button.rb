require 'nokogiri'

Jekyll::Hooks.register :pages, :post_convert do |page|
  btn_text = '<button class="copy-button hidden" aria-label="copy code to clipboard" type="button" aria-hidden="true">' \
    '<div class="copy-button-inner">' \
    '<svg width="12" height="12" viewBox="340 364 14 15" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M342 375.974h4v.998h-4v-.998zm5-5.987h-5v.998h5v-.998zm2 2.994v-1.995l-3 2.993 3 2.994v-1.996h5v-1.995h-5zm-4.5-.997H342v.998h2.5v-.997zm-2.5 2.993h2.5v-.998H342v.998zm9 .998h1v1.996c-.016.28-.11.514-.297.702-.187.187-.422.28-.703.296h-10c-.547 0-1-.452-1-.998v-10.976c0-.546.453-.998 1-.998h3c0-1.107.89-1.996 2-1.996 1.11 0 2 .89 2 1.996h3c.547 0 1 .452 1 .998v4.99h-1v-2.995h-10v8.98h10v-1.996zm-9-7.983h8c0-.544-.453-.996-1-.996h-1c-.547 0-1-.453-1-.998 0-.546-.453-.998-1-.998-.547 0-1 .452-1 .998 0 .545-.453.998-1 .998h-1c-.547 0-1 .452-1 .997z" fill-rule="evenodd"/></svg>' \
    '<strong class="copy-button-label"></strong></div></button>'
  parsed_data = Nokogiri::HTML.parse(page.content)
  codeblocks = parsed_data.xpath("//div[@class='listingblock']")
  codeblocks.each do |block|
    btn = Nokogiri::XML::DocumentFragment.parse(btn_text).at_css("button")
    block.children.first.add_previous_sibling(btn)
  end
  if page.content
    page.content = parsed_data.to_html
  end
end 
