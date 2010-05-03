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
version = cgi.params['version'][0].to_i

files = []
files << "../data/#{name_id}/#{title_id}"

backups = []
if File.exist?("../data/#{name_id}/backups/#{title_id}") then
  Dir.open("../data/#{name_id}/backups/#{title_id}").each { |f|
    backups << f if f =~ /^.{14}$/
  }
end
backups.sort{ |a,b|
  b <=> a
}.each { |f|
  files << "../data/#{name_id}/backups/#{title_id}/#{f}"
}

if version >= files.length then
  version = files.length-1
end
file = files[version]

data = ''
begin
  data = File.open(file).read
rescue
end

if version > 0 then
  dbm = SDBM.open("../data/#{name_id}/backups/#{title_id}/timestamp",0644)
  a = ''
  data.each { |line|
    l = line.chomp
    ll = l.sub(/^\s*/,'')
    dbm[ll] =~ /(....)(..)(..)(..)(..)(..)/
    t = Time.local($1.to_i,$2.to_i,$3.to_i,$4.to_i,$5.to_i,$6.to_i)
    td = (Time.now - t).to_i
    a += "#{l} #{td}\n"
  }
  dbm.close
  data = a
end

data_md5 = Digest::MD5.new.hexdigest(data)
out = "#{data_md5}\n"

if version > 0
  file =~ /(\d{14})$/
  out << "#{$1}\n"
end

s = data.gsub(/[\s\r\n]/,'')
if s.length == 0 then
  out << '(empty)'
else
  out << data
end

out = "\xef\xbb\xbf" + out # BOM

cgi.out {
  out
}

