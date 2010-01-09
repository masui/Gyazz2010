#!/usr/bin/env ruby
# -*- ruby -*-
#
# $Date$
# $Rev$
#
require 'cgi'
require 'digest/md5'
require 'html'
require 'pair'
require 'set'

def md5(name)
  Digest::MD5.new.hexdigest("#{name}").to_s
end

cgi = CGI.new("html3")
name = cgi.params['name'][0].to_s        # Wikiの名前   (e.g. masui)
name_id = md5(name)                      # そのMD5値    (e.g. 451dc4c8383accedc009c9d6b334d851)
q = cgi.params['q'][0].to_s

GYAZZTOP = "http://gyazz.com"
wikitop = "../data/#{name_id}"
urltop = "http://gyazz.com/#{name}"
if !File.directory?(wikitop) then
  Dir.mkdir(wikitop)
end

sh = SimpleHtmlGenerator.new

pair = Pair.new("#{wikitop}/pair")

titles = Set.new
pair.each { |key1,key2|
  titles.add(key1) if key1
  titles.add(key2) if key2
}

id2title = {}
titles.each { |title|
  id2title[md5(title)] = title
}

if !File.directory?(wikitop) then
  Dir.mkdir(wikitop)
end

ids = Dir.open(wikitop).find_all { |file|
  file =~ /^[\da-f]{32}$/ && id2title[file].to_s != ''
}

modtime = {}
ids.each { |id|
  modtime[id] = File.mtime("#{wikitop}/#{id}")
}

hotids = ids.sort { |a,b|
  modtime[b] <=> modtime[a]
}

matchids = hotids
if q != '' then
  matchids = hotids.find_all { |id|
    title = id2title[id]
    content = File.read("#{wikitop}/#{id}")
    #title.index(q) || content.index(q)
    title.match(/#{q}/i) || content.match(/#{q}/i)
  }
end

s = matchids.collect { |id|
  title = id2title[id]
  url = "#{urltop}/#{CGI.escape(title)}".gsub(/%2F/,"/")
  "<div class=\"listedit0\"><a href=\"#{url}\" class='tag'>#{title}</a></div>\n"
#  "<div class=\"listedit0\"><a href=\"#{urltop}/#{CGI.escape(title)}\" class='tag'>#{title}</a></div>\n"
}.join

length = matchids.length

cgi.out {
  sh.html {
    sh.head {
      sh.meta('http-equiv' => "Content-Type", 'content' => "text/html; charset=utf-8") +
      sh.title{ 'Search Result' } +
      sh.link('rel' => "stylesheet", 'href' => "#{GYAZZTOP}/stylesheets/page.css", 'type' => "text/css; charset=utf-8")
    } +
    sh.body {
      sh.div('class' => 'title'){
        sh.span('class' => 'wordtitle'){ "検索結果 (#{length})" } +
        sh.form('action' => "#{GYAZZTOP}/programs/search.cgi", 'method' => "get", 'style' => "float:right;font-size:12pt;"){
          sh.input('height' => '20', 'name' => 'q', type => 'text', 'value' => q) + ' ' +
          # sh.input('name' => 'commit', 'type' => 'submit', 'value' => '検索')
          sh.input('type' => 'submit', 'value' => '検索') +
          sh.input('name' => 'name', 'type' => 'hidden', 'value' => name)
        }
      } +
      sh.p +
      s
    }
  }
}

