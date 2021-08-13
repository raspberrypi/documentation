require 'nokogiri'

Jekyll::Hooks.register :pages, :post_convert do |page|
  link_text = '<a id="" href="" class="doc-anchor" aria-hidden="true">' \
    '<svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true">' \
    '<path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z">' \
    '</path></svg></a>'
  parsed_data = Nokogiri::HTML.parse(page.content)
  headings = parsed_data.xpath("//div[@class='sect1']/h2|//div[@class='sect2']/h3|//div[@class='sect3']/h4|//div[@class='sect4']/h5|//div[@class='sect5']/h6")
  headings.each do |heading|
    link = Nokogiri::XML::DocumentFragment.parse(link_text).at_css("a")
    id = heading.attr('id') + "_anchor"
    href = "#" + heading.attr('id')
    link["id"] = id
    link["href"] = href
    heading.children.first.add_previous_sibling(link)
  end
  if page.content
    page.content = parsed_data.to_html
  end
end