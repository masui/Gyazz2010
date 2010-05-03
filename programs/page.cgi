#!/usr/bin/env ruby
# -*- ruby -*-
#
# $Date$
# $Rev$
#
require 'cgi'
require 'digest/md5'
require 'html'
require 'keyword'
require 'pair'
require 'sdbm'
require 'config'

$KCODE = 'u'

def md5(s)
   Digest::MD5.new.hexdigest(s).to_s
end

cgi = CGI.new("html3")
sh = SimpleHtmlGenerator.new

name = cgi.params['name'][0].to_s        # Wikiの名前   (e.g. masui)
name_id = md5(name)                      # そのMD5値    (e.g. 451dc4c8383accedc009c9d6b334d851)
title = cgi.params['title'][0].to_s      # ページの名前 (e.g. TODO)
title_id = md5(title)                    # そのMD5値    (e.g. b7b1e314614cf326c6e2b6eba1540682)
version = cgi.params['version'][0].to_i
filename = "../data/#{name_id}/#{title_id}"

if name =~ /AddLink-Mark/ || title =~ /AddLink-Mark/ then
  cgi.out { '' }
  exit
end

gyazoid = nil
cookies = cgi.cookies['GyazoID']
if cookies then
  gyazoid = cookies.first.to_s
end

#File.open("/tmp/aaaaaaaaaaaa","w"){ |f|
# f.puts gyazoid
#}

File.open("../log/log","a"){ |f|
  f.puts "#{Time.now}\t#{ENV['REMOTE_ADDR']}\t#{name}/#{title}"
}

search = ''

require 'uri'
require 'set'

wikitop = "../data/#{name_id}"
urltop = "#{GYAZZTOP}/#{name}"
if !File.directory?(wikitop) then
  Dir.mkdir(wikitop)
end

pair = Pair.new("#{wikitop}/pair")

pagekeywords = []
if File.exist?(filename) then
  pagekeywords = File.read(filename).keywords
  File.utime(Time.now,Time.now,filename)
end

#
# http://pitecan.com/~masui/Wiki/リンク重要度計算
#
linkcount = {}
pair.each { |key1,key2|
  linkcount[key1] = 0.0 unless linkcount[key1]
  linkcount[key2] = 0.0 unless linkcount[key2]
  linkcount[key1] += 1.0
  linkcount[key2] += 1.0
}

linkcount2 = {}
pair.each { |key1,key2|
  linkcount2[key1] = 0.0 unless linkcount2[key1]
  linkcount2[key2] = 0.0 unless linkcount2[key2]
  linkcount2[key1] += linkcount[key2]
  linkcount2[key2] += linkcount[key1]
}
#File.open("/tmp/xxxx","w"){ |f|
#  pair.each { |key1,key2|
#    f.puts "#{key1}, #{key2}"
#  }
#}

weight = {}
pair.each(title) { |key|
next if key =~ /^@/ # 苦しい。pairをクリアしなければ
next if key =~ /::/ # 苦しい。pairをクリアしなければ
  weight[key] = linkcount[key]
}
newweight = {}
pair.each { |key1,key2|
  if weight[key1] && !weight[key2] then
    newweight[key2] = 0.0 unless newweight[key2]
    newweight[key2] += linkcount[key2] / linkcount2[key1]
  end
  if weight[key2] && !weight[key1] then
    newweight[key1] = 0.0 unless newweight[key1]
    newweight[key1] += linkcount[key1] / linkcount2[key2]
  end
}
newweight.each { |key,val|
  weight[key] = val
}

weight.delete(title)

require 'sdbm'
repimage = SDBM.open("#{wikitop}/repimage",0644)

uploadedimages = ''
if gyazoid then
  idimage = SDBM.open("../data/idimage",0644)
  uploadedimages = idimage[gyazoid].to_s.split(/,/).collect { |id|
  # ondragendはFirefox3.1以降
  <<EOF
<div style="height:64;width:64;margin:2;float:left">
<center>
<!--a href='http://gyazo.com/#{id}.png'-->
<img src='http://gyazo.com/#{id}.png'
style='max-height:64;max-width:64;border:none;width:expression(document.body.clientWidth < 64? "64px" : document.body.clientWidth > 64? "64px" : "auto");'
ondragend = 'addimage("#{id}")'
onclick='location.href="http://gyazo.com/#{id}.png"'>
<!--/a-->
</center>
</div>
EOF
  }.join('')
  uploadedimages = <<EOF
<div class='links'>
#{uploadedimages}
<p>
<br clear='all'>
</div>
EOF
end

links = weight.keys.sort { |key1,key2|
  weight[key2] <=> weight[key1]
}.collect { |t|
  url = "#{urltop}/#{CGI.escape(t)}".gsub(/%2F/,"/") # '?'がデコードされない
  if repimage[t] then
    sh.a!('href' => "#{url}"){ 
<<EOF
<div style="height:64;width:64;margin:2;float:left">
<center>
<img src='http://gyazo.com/#{repimage[t]}.png'
title='#{t}'
style='max-height:64;max-width:64;border:none;width:expression(document.body.clientWidth < 64? "64px" : document.body.clientWidth > 64? "64px" : "auto");'>
</center>
</div>
EOF
    }
  else
    length = t.split(//).length
    fontsize = (length <= 2 ? 20 : length < 4 ? 14 : 10)
    fontsize = 9
 targetid = md5(t)
 r = (targetid[0..1].hex.to_f * 0.5 + 16).to_i.to_s(16)
 g = (targetid[2..3].hex.to_f * 0.5 + 16).to_i.to_s(16)
 b = (targetid[4..5].hex.to_f * 0.5 + 16).to_i.to_s(16)
<<EOF
<a href="#{url}" class="links">
<div style="height:64;width:64;margin:2;float:left;background-color:##{r}#{g}#{b};">
<div style="font-size:#{fontsize}pt;margin:3;color:white;">
#{t}
</div>
</div>
</a>
EOF
  end
}.join(' ')

attr = SDBM.open("../data/#{name_id}/attr",0644)
robotsattr = (attr['searchable'] == 'true' ? "index,follow" : "noindex,nofollow")

cgi.out('Pragma' => 'no-cache', 'Cache-Control' => 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0', 'Expires' => 'Thu, 01 Dec 1994 16:00:00 GMT'){
  sh.html {
    sh.head {
      sh.meta('http-equiv' => "Content-Type", 'content' => "text/html; charset=utf-8") + "\n" +
      sh.meta('http-equiv' => "pragma", 'content' => "no-cache") + "\n" +
      sh.meta('http-equiv' => "cache-control", 'content' => "no-cache") + "\n" +
      sh.meta('http-equiv' => "cache-control", 'content' => "no-store") + "\n" +
      sh.meta('http-equiv' => "cache-control", 'content' => "must-revalidate") + "\n" +
      sh.meta('http-equiv' => "Expires", 'content' => "Thu, 01 Dec 1994 16:00:00 GMT") + "\n" +
      sh.meta('name' => "robots", 'content' => "#{robotsattr}") + "\n" +
      sh.title{ title } + "\n" +
      sh.link('rel' => "stylesheet", 'href' => "#{GYAZZTOP}/stylesheets/page.css", 'type' => "text/css; charset=utf-8") + "\n" +
      sh.link('rel' => "stylesheet", 'href' => "#{GYAZZTOP}/#{name}/.CSS/text", 'type' => "text/css; charset=utf-8") + "\n" +
      sh.script('src' => "#{GYAZZTOP}/javascripts/pbdict.js", 'type' => 'text/javascript'){ } + "\n" +
      sh.script('src' => "#{GYAZZTOP}/javascripts/pbsearch.js", 'type' => 'text/javascript'){ } + "\n" +
      sh.script('src' => "#{GYAZZTOP}/javascripts/utf.js", 'type' => 'text/javascript'){ } + "\n" +
      sh.script('src' => "#{GYAZZTOP}/javascripts/md5.js", 'type' => 'text/javascript'){ } + "\n" +
      sh.script('src' => "#{GYAZZTOP}/javascripts/listedit.js", 'type' => 'text/javascript'){ } + "\n" +
      sh.script('type' => 'text/javascript'){
         name_escape = name.gsub(/'/,'\\\\\'')
         title_escape = title.gsub(/'/,'\\\\\'')
         "var name = '#{name_escape}';\n" +
         "var title = '#{title_escape}';\n" +
         "var version = #{version};\n" +
         "var TOP = #{GYAZZTOP};\n"
      }
    } +
    sh.body {
      sh.div('class' => 'title'){
        sh.span('class' => 'wordtitle'){ 
          sh.a('href' => "#{GYAZZTOP}/#{name}/#{CGI.escape(title).gsub(/%2F/,'/')}/edit"){
            title
          }
        } +
        sh.form('action' => "#{GYAZZTOP}/programs/search.cgi", 'method' => "get", 'style' => "float:right;font-size:12pt;"){
          sh.input('height' => '20', 'name' => 'q', 'type' => 'text') + ' ' +
#          sh.input('name' => 'commit', 'type' => 'submit', 'value' => '検索') +
          sh.input('type' => 'submit', 'value' => '検索') +
          sh.input('name' => 'name', 'type' => 'hidden', 'value' => name)
        } +
        sh.span('class' => 'language', 'id' => 'datestr'){ }
      } +
      sh.p +
      search +
      sh.div('id' => 'querydiv'){ } +
      sh.div('id' => 'contents'){ } +
      sh.input('type' => 'text',
               'id' => 'newtext',
               'onmousedown' => 'editing=true',
               'autocomplete' => 'off',
               'style' => "font-size:10pt;position:absolute;width:600;visibility:hidden;border:none;padding:1px;margin:0;background-color:#ddd;") +
      sh.p +
#      sh.div('class' => 'links'){
#        uploadedimages + sh.p + "<br clear='all'>"
#      } +
#      sh.p +
      sh.div('class' => 'links'){
#        uploadedimages +
        links + sh.p + "<br clear='all'>"
      } +
      sh.p + uploadedimages +
      sh.script('type' => 'text/javascript'){
        "setup(); getdata();"
      }
    }
  }
}


