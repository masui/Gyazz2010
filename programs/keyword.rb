class String
  def keywords
    s = self.dup
    a = []
    while s.sub!(/\[\[\[[^\]\n\r]+\]\]\]/,'') do
    end
    while s.sub!(/\[\[([^\[\n\r ]+\/) [^\]]+\]\]/,'') do
      kw = $1
      if kw !~ /^http/ && kw !~ /pdf / && kw !~ /^@/ && kw !~ /::/ then
        a << kw
      end
    end
    while s.sub!(/\[\[([^\[\n\r]+)\]\]/,'') do
      kw = $1
      if kw !~ /^http/ && kw !~ /pdf / && kw !~ /^@/ && kw !~ /::/ then
        a << kw
      end
    end
    a
  end
end
