#!/usr/bin/env ruby
# -*- ruby -*-
#
# $Date$
# $Rev$
#
require 'cgi'
require 'sdbm'
require 'html'
require 'digest/md5'

cgi = CGI.new("html3")

name = cgi.params['name'][0].to_s
name_id = Digest::MD5.new.hexdigest(name).to_s
protected = cgi.params['protected'][0].to_s

attr = SDBM.open("../data/#{name_id}/attr",0666);
attr['protected'] = protected;

cgi.out { '' }
