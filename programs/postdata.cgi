#!/usr/bin/env ruby
# -*- ruby -*-
#
# $Date$
# $Rev$
#
require 'cgi'
require 'digest/md5'
require 'keyword'
require 'set'
require 'pair'
require 'sdbm'
require 'set'

cgi = CGI.new("html3")

data = cgi.params['data'][0].split(/\n/)
name = data.shift
name_id = Digest::MD5.new.hexdigest(name).to_s
title = data.shift
title_id = Digest::MD5.new.hexdigest(title).to_s
file = "../data/#{name_id}/#{title_id}"

gyazoid = nil
cookies = cgi.cookies['GyazoID']
if cookies then
  gyazoid = cookies.first.to_s
end

def writable?(id,gyazoid)
  attr = SDBM.open("../data/#{id}/attr",0644)
  return true if attr['protected'] != 'true'

  gyazoids = Set.new
  imageid = SDBM.open("../data/imageid",0644)
  Dir.open("../data/#{id}").each { |f|
    if f =~ /^[0-9a-f]{32}$/ then
      filename = "../data/#{id}/#{f}"
      if File.file?(filename) then
        File.open(filename){ |f|
          f.each { |line|
            while line.sub!(/http:\/\/gyazo.com\/([0-9a-f]{32}).png/,'') do
              iid = $1
              if imageid[iid] then
  	        gyazoids.add(imageid[iid])
              end
            end
          }
        }
      end
    end
  }
  gyazoids.member?(gyazoid)
end

if !writable?(name_id,gyazoid) then
  cgi.out { '' }
  exit
end

# バックアップ作成

timestamp = Time.now.strftime('%Y%m%d%H%M%S')

backupsdir = "../data/#{name_id}/backups"
backupdir = "../data/#{name_id}/backups/#{title_id}"
backupfile = "#{backupdir}/#{timestamp}"

unless File.exist?(backupsdir) then
  Dir.mkdir(backupsdir)
end
unless File.exist?(backupdir) then
  Dir.mkdir(backupdir)
end

dbm = SDBM.open("#{backupdir}/timestamp",0644)
data.each { |line|
  l = line.sub(/^\s*/,'')
  if !dbm[l] then
    dbm[l] = timestamp
  end
}
dbm.close

curdata = ''
newdata = data.join("\n")

if File.exist?(file) then
  curdata = File.read(file)
  if curdata != newdata then
    File.open(backupfile,'w').print(curdata)
  end
end

mykeyword = title

pair = Pair.new("../data/#{name_id}/pair")

curdata.keywords.each { |keyword|
  pair.delete(mykeyword,keyword)
}

newdata.keywords.each { |keyword|
  pair.add(mykeyword,keyword)
}

#
# repimage
#

repimage = SDBM.open("../data/#{name_id}/repimage",0644)
if data[0] =~ /gyazo.com\/(\w{32})\.png/i then
  repimage[title] = $1
else
  repimage.delete(title)
end


# if title != '類語をみつける方法' then
  File.open(file,"w"){ |f|
    f.print newdata
  }
# end

cgi.out {
  ''
}
