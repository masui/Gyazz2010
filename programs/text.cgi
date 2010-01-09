#!/usr/bin/env ruby
# -*- ruby -*-
#
# $Date$
# $Rev$
#
require 'cgi'
require 'sdbm'
require 'digest/md5'

cgi = CGI.new("html3")

name = cgi.params['name'][0].to_s
name_id = Digest::MD5.new.hexdigest(name).to_s
title = cgi.params['title'][0].to_s
title_id = Digest::MD5.new.hexdigest(title).to_s

file = "../data/#{name_id}/#{title_id}"
data = ''
begin
  data = File.open(file).read
rescue
end

# data = "\xef\xbb\xbf" + data # BOM

cgi.out({"charset" => "utf-8"}){
  data
}


