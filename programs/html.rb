# -*- ruby -*-

class SimpleHtmlGenerator
  def initialize
  end

  def doctype
    '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">'
  end

  def css (url)
    %Q(<link rel=stylesheet href="#{url}" media=all>)
  end

  def dtd
    %Q(<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/strict.dtd">)
  end

  def method_missing (symbol, *args)
    element = symbol.to_s
    compact = false
    delim = "\n"
    indent = " "
    if element =~ /\!$/ then
      element.sub!(/\!$/,'')
      compact = true
      delim = ''
      indent = ''
    end

indent = ''
delim = '' if element == 'textarea'

    if block_given?
      s = yield
      s = '' if s.nil?
      s = s.to_s
      if args.empty?
        "<#{element}>" + delim +
        (element == 'textarea' ?  s : 
        s.split(/\r?\n/).collect{ |s| indent + s }.join("\n")) + delim +
        "</#{element}>" + delim
      else
        indent + "<#{element} " +
        args.first.map {|key, value| "#{key}='#{value}'"}.join(" ") + ">" + delim +
        s.split(/\r?\n/).collect{ |s| indent + s }.join("\n") + delim +
        indent + "</#{element}>" + delim
      end
    else
      if args.empty?
        "<#{element}>" + delim
      else
        "<#{element} " +
          args.first.map {|key, value| "#{key}='#{value}'"}.join(" ") + 
          ">"
      end
    end
  end
end

