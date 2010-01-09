#!/usr/bin/env ruby
# -*- ruby -*-
#
# $Date$
# $Rev$
#

#
# ローカルのGyazoからこのCGIが呼ばれると、
#  - ローカルGyazoのID
#  - アップする画像のURL
# が取得される。
# IDはブラウザのCookieに保存しておく。Gyazzアクセスのとき、そのIDのものをリストすることにする。
#

require 'cgi'
require 'html'
require 'sdbm'

$KCODE = 'u'

cgi = CGI.new("html3")
sh = SimpleHtmlGenerator.new

gyazoid = cgi.params['gyazoid'][0].to_s
url = cgi.params['url'][0].to_s

# GyazoID(アプリのID)とurlの対応関係を保存しておく
url =~ /([\da-f]{32})/
id = $1
idimage = SDBM.open("../data/idimage",0644)
idimage[gyazoid] = idimage[gyazoid].to_s.split(/,/).unshift(id)[0,5].join(',')

# 画像URLとGyazoIDの対応も保存する
imageid = SDBM.open("../data/imageid",0644)
imageid[id] = gyazoid

# Cookieをブラウザに渡しつつMOVEDでGyazoにジャンプする
cookie = CGI::Cookie.new({"name" => "GyazoID", "value" => gyazoid, "path" => "/"})
cgi.out({"cookie" => [cookie], 'status' => 'MOVED', 'Location' => url, 'Time' => Time.now}){
  ''
}

