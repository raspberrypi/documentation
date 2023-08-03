module Slim::Helpers
  def book_link
    puts (self.attr 'booktype')
    puts (document.attr 'booktype')
    case (self.attr 'booktype')
    when 'free'
      %("FREEEEEEE")
    when 'buy'
      %("BUY TEXT")
    when 'donate'
      %("DONATE")
    else
      %("NONE")
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