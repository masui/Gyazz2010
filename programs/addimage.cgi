#!/usr/bin/env ruby
# -*- ruby -*-
#
# $Date$
# $Rev$
#
require 'cgi'
require 'digest/md5'
require 'html'

GYAZZTOP = "http://gyazz.com"

def md5(s)
  Digest::MD5.new.hexdigest(s).to_s
end

cgi = CGI.new("html3")

imageurl = cgi.params['imageurl'][0].to_s
name = cgi.params['name'][0].to_s        # Wikiの名前   (e.g. masui)
name_id = md5(name)                      # そのMD5値    (e.g. 451dc4c8383accedc009c9d6b334d851)
title = cgi.params['title'][0].to_s      # ページの名前 (e.g. TODO)
title_id = md5(title)                    # そのMD5値    (e.g. b7b1e314614cf326c6e2b6eba1540682)

filename = "../data/#{name_id}/#{title_id}"
wikitop = "../data/#{name_id}"
urltop = "http://gyazz.com/#{name}"

data = ''
if File.exist?(filename) then
  data = File.read(filename)
end
File.open(filename,"w"){ |f|
  f.print data + "\n[[#{imageurl}]]"
}

cgi.out { '' }


