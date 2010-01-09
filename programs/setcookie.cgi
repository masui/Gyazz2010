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

$KCODE = 'u'

cgi = CGI.new("html3")
sh = SimpleHtmlGenerator.new

gyazoid = cgi.params['gyazoid'][0].to_s
url = cgi.params['url'][0].to_s
# ここでGyazoIDとurlの対応関係はわかるわけね。保存しておけばいいわけだ

cookie = CGI::Cookie.new({"name" => "GyazoID", "value" => gyazoid})

cgi.out({"cookie" => [cookie], 'status' => 'MOVED', 'Location' => url, 'Time' => Time.now}){
  ''
}

