#!/usr/bin/env ruby
# -*- ruby -*-
#
# $Date$
# $Rev$
#
require 'cgi'
require 'html'

$KCODE = 'u'

cgi = CGI.new("html3")
sh = SimpleHtmlGenerator.new

gyazoid = cgi.params['gyazoid'][0].to_s

values = cgi.cookies['GyazoID'] 

cookie = CGI::Cookie.new({"name" => "GyazoID", "value" => "2009123"})

cgi.out({"cookie" => [cookie]}){
 <<EOF
abcdefg
<p>
#{values.collect {|val| val }}
EOF
}

