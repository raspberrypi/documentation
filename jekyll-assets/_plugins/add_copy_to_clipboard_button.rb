require 'nokogiri'

Jekyll::Hooks.register :pages, :post_convert do |page|
  btn_text = '<button class="copy-button hidden" aria-label="copy code to clipboard" type="button" aria-hidden="true">' \
    '<div class="copy-button-inner">' \
    '<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12"><rect x="1" y="6" width="5" height="1"/><path d="M10,1H8A1,1,0,0,0,7,0H6A1,1,0,0,0,5,1H3A1,1,0,0,0,2,2V5H3V2H4V3H9V2h1v9H3V8H2v3a1,1,0,0,0,1,1h7a1,1,0,0,0,1-1V2A1,1,0,0,0,10,1ZM6.5,2.25a.75.75,0,1,1,.75-.75A.76.76,0,0,1,6.5,2.25Z"/><path d="M6.32,6.32,4.43,4.43A.25.25,0,0,0,4,4.6V8.4a.25.25,0,0,0,.43.17L6.32,6.68A.25.25,0,0,0,6.32,6.32Z"/></svg>' \
    '<strong class="copy-button-label"></strong><span class="tooltip hidden"> Copy to Clipboard</span></div></button>'
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
