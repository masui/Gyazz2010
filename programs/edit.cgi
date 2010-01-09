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
sh = SimpleHtmlGenerator.new

data = cgi.params['data'][0].to_s
name = cgi.params['name'][0].to_s        # Wikiの名前   (e.g. masui)
name_id = md5(name)                      # そのMD5値    (e.g. 451dc4c8383accedc009c9d6b334d851)
title = cgi.params['title'][0].to_s      # ページの名前 (e.g. TODO)
title_id = md5(title)                    # そのMD5値    (e.g. b7b1e314614cf326c6e2b6eba1540682)
version = cgi.params['version'][0].to_i
filename = "../data/#{name_id}/#{title_id}"

wikitop = "../data/#{name_id}"
urltop = "http://gyazz.com/#{name}"

if data == '' then
  begin
    data = File.open(filename).read
  rescue
  end
end

cgi.out {
  sh.html {
    sh.head {
      sh.meta('http-equiv' => "Content-Type", 'content' => "text/html; charset=utf-8") +
      sh.title{ "#{name}/#{title}" } +
      sh.link('rel' => "stylesheet", 'href' => "#{GYAZZTOP}/stylesheets/page.css", 'type' => "text/css; charset=utf-8") +
      sh.script('src' => "#{GYAZZTOP}/javascripts/edit.js", 'type' => 'text/javascript'){ } +
      sh.script('type' => 'text/javascript'){
         name_escape = name.gsub(/'/,'\\\\\'')
         title_escape = title.gsub(/'/,'\\\\\'')
         "var name = '#{name_escape}';\n" +
         "var title = '#{title_escape}';\n"
      }
    } +
    sh.body {
      sh.div('class' => 'title'){
        sh.span('class' => 'wordtitle'){ 
          sh.span('class' => 'wordtitle'){ 
            sh.a('href' => "#{GYAZZTOP}/#{name}/#{CGI.escape(title).gsub(/%2F/,'/')}"){
              title
            }
          }
        } +
        sh.form('action' => "#{GYAZZTOP}/programs/search.cgi", 'method' => "get", 'style' => "float:right;font-size:12pt;"){
          sh.input('height' => '20', 'name' => 'q', type => 'text') + ' ' +
          sh.input('name' => 'commit', 'type' => 'submit', 'value' => '検索') +
          sh.input('name' => 'name', 'type' => 'hidden', 'value' => name)
        }
      } +
      sh.p +
      sh.textarea('id' => 'contents', 'cols' => '100', 'rows' => '40') {
        data
      }
    }
  }
}

