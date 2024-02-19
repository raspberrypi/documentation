require 'net/http'
require 'json'

module Slim::Helpers
  def book_link
    case (self.attr 'booktype')
    when 'free'
      %(You can <a href="#{self.attr 'link'}" target="_blank">download this book</a> as a PDF file for free, it has been released under a Creative Commons <a href="https://creativecommons.org/licenses/by-nc-sa/3.0/" target="_blank">Attribution-NonCommercial-ShareAlike</a> 3.0 Unported (CC BY NC-SA) licence.)
    when 'buy'
      %(You can <a href="#{self.attr 'link'}" target="_blank">buy this book</a> on the Raspberry Pi Press site.)
    when 'donate'
      %(You can <a href="#{self.attr 'link'}" target="_blank">download this book</a> for an optional donation on the Raspberry Pi Press site.)
    else
      return
    end
  end

  def book_image
    src = (self.attr 'image').dup
    src = src.gsub(/^image::/, "")
    src = src.gsub(/\[.*?\]$/, "")
    return src
  end

  def tutorial_image
    desc = ""
    img_src = ""
    # hit the api
    res = Net::HTTP.get_response(URI("https://www.raspberrypi.com/tutorials/api.json"))
    data = JSON.parse(res.body)
    record = data.select {|item| item["url"] == (self.attr 'link')}
    if record.length() > 0
      desc = record[0]["excerpt"]
      img_src = record[0]["featuredImageUrl"]
    end
    return '<a href="'+(self.attr 'link')+'" target="_blank" class="image"><div class="tutorialcard"><img src="'+img_src+'"/><p class="caption">'+desc+'</p></div></a>'
  end

  def tutorial_image_sidebar
    uri = URI(self.attr 'link')
    source = Net::HTTP.get(uri)
    # get the image source
    img_src = ""
    img_arr = /<meta[^>]+property="og:image"[^>]+content="([^>]+)"[^>]*>/.match(source)
    if img_arr
      img_src = img_arr[1]
    end
    return '<a href="'+(self.attr 'link')+'" target="_blank" class="image"><div class="tutorialcard"><img src="'+img_src+'"/></div></a>'
  end

  def tutorial_description_sidebar
    uri = URI(self.attr 'link')
    source = Net::HTTP.get(uri)
    # get the short description
    desc = ""
    desc_arr = /<meta[^>]+name="description"[^>]+content="([^>]+)"[^>]*>/.match(source)
    if desc_arr
      desc = desc_arr[1]
    end
    return '<div class="paragraph tutorialdescription"><p>'+desc+'</p></div>'
  end

  def section_title
    if caption
      captioned_title
    elsif numbered && level <= (document.attr :sectnumlevels, 3).to_i
      if level < 2 && document.doctype == 'book'
        case sectname
        when 'chapter'
          %(#{(signifier = document.attr 'chapter-signifier') ? signifier.to_s + ' ' : ''}#{sectnum} #{title})
        when 'part'
          %(#{(signifier = document.attr 'part-signifier') ? signifier.to_s + ' ' : ''}#{sectnum nil, ':'} #{title})
        else
          %(#{sectnum} #{title})
        end
      else
        %(#{sectnum} #{title})
      end
    else
      title
    end
  end
end