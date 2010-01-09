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

file = "../data/#{name_id}/#{title_id}"
text = ''
begin
  text = File.open(file).read
rescue
end

list = text.split(/\n/)

image = []
posx = []
posy = []
width = []
comment = []
time = []
color = []
ind = 0
oldind = 0
comment[0] = ''

list.each { |line|
  if line =~ /http:\S*\.(png|jpg|gif)/ then
    oldind = ind
    image[ind] = $&
    posx[ind] = '5%'
    posy[ind] = '5%'
    width[ind] = '90%'
    color[ind] = '#ffffff'
    comment[ind] = ''
    time[ind] = 5
    ind += 1
  elsif line =~ /([\d\.]+%?)\s+([\d\.]+%?)\s+([\d\.]+%?)/ then
    posx[oldind] = $1
    posy[oldind] = $2
    width[oldind] = $3
  elsif line =~ /^\s*([\d\.]+)S/ then
    time[oldind] = $1
  elsif line =~ /^\s*(#[\da-zA-Z]+)/ then
    color[oldind] = $1
  else
    comment[oldind] += '<br>' if comment[oldind] != ''
    comment[oldind] += line.gsub(/'/,"\\'")
  end
}

s = (0...ind).collect { |i|
  <<EOF
image[#{i}] = '#{image[i]}';
top[#{i}] = '#{posx[i]}';
left[#{i}] = '#{posy[i]}';
width[#{i}] = '#{width[i]}';
color[#{i}] = '#{color[i]}';
comment[#{i}] = '#{comment[i]}';
sleep[#{i}] = '#{time[i]}';
EOF
}.join("\n")

cgi.out {
  <<EOF
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width user-scalable=no">
<title>#{title}</title>
<script type="text/javascript">
</script>
<style type="text/css">
<!--
img {
  position:absolute;
  top:0;
  left:0;
  width:100%;
}
div {
  position:absolute;
  color:white;
  font-size:20pt;
}
-->
</style>
</head>
<body style="margin:0;border:0;padding:0;overflow:hidden;">

<img id='photo'>
<div id='comment'></div>

<script type="text/javascript">
var image = [];
var top = [];
var left = [];
var width = [];
var comment = [];
var color = [];
var sleep = [];
var cur = 0;

//
#{s}
//

var photo = document.getElementById('photo');
var c = document.getElementById('comment');

function display(){
  photo.src = image[cur];
  c.style.top = top[cur];
  c.style.left = left[cur];
  c.style.width = width[cur];
  c.style.fontSize = '20pt';
  c.style.color = color[cur];
  c.innerHTML = comment[cur];
  setTimeout(display,sleep[cur] * 1000);
  cur += 1;
  if(cur >= image.length) cur = 0;
}

display();

window.onload = function(){setTimeout(hideURLbar,100);}
window.onorientationchange = hideURLbar;
//画面が横←→縦に変化したとき呼び出される。
function hideURLbar() { window.scrollTo(0,1);}
</script>

</body>
</html>
EOF
}
