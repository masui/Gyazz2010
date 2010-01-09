#!/usr/bin/env ruby
# -*- ruby -*-
#
# $Date$
# $Rev$
#
require 'cgi'
require 'html'
require 'sdbm'

$KCODE = 'u'

cgi = CGI.new("html3")
sh = SimpleHtmlGenerator.new

values = cgi.cookies['GyazoID'] 

idimage = SDBM.open("../data/idimage",0644)

cgi.out {
 <<EOF
ID is
<p>
#{idimage[values.first]}
EOF
}

