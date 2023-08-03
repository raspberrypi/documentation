module Slim::Helpers
  def book_link
    case (self.attr 'booktype')
    when 'free'
      %(You can <a href="#{self.attr 'link'}" target="_blank">download this book</a> as a PDF file for free, it has been released under a Creative Commons <a href="https://creativecommons.org/licenses/by-nc-sa/3.0/" target="_blank">Attribution-NonCommercial-ShareAlike</a> 3.0 Unported (CC BY NC-SA) licence.)
    when 'buy'
      %(You can <a href="#{self.attr 'link'}" target="_blank">buy this book</a> on the Raspberry Pi Press site.)
    when 'donate'
      %(You can <a href="#{document.attr 'link'}" target="_blank">download this book</a> for an optional donation on the Raspberry Pi Press site.)
    else
      return
    end
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