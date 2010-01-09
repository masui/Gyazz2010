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

GYAZZTOP = "http://gyazz.com"

cgi = CGI.new("html3")
sh = SimpleHtmlGenerator.new

name = cgi.params['name'][0].to_s
name_id = Digest::MD5.new.hexdigest(name).to_s

attr = SDBM.open("../data/#{name_id}/attr",0644);

cgi.out {
  sh.html {
    sh.head {
      sh.meta('http-equiv' => "Content-Type", 'content' => "text/html; charset=utf-8") +
      sh.title{ name } +
      sh.link('rel' => "stylesheet", 'href' => "#{GYAZZTOP}/stylesheets/page.css", 'type' => "text/css; charset=utf-8")
    } +
    sh.body {
      sh.div('class' => 'title'){
        sh.span('class' => 'wordtitle'){ 
          name + ' ' + '設定'
        } +
        sh.form('action' => "#{GYAZZTOP}/programs/search.cgi", 'method' => "get", 'style' => "float:right;font-size:12pt;"){
          sh.input('height' => '20', 'name' => 'q', type => 'text') + ' ' +
          sh.input('name' => 'commit', 'type' => 'submit', 'value' => '検索') +
          sh.input('name' => 'name', 'type' => 'hidden', 'value' => name)
        } +
        sh.span('class' => 'language', 'id' => 'datestr'){ }
      } +
      sh.p +
      sh.input('id' => 'protected', 'type' => 'checkbox', 'checked' => '') + '編集を制限する' +
<<EOF
<script type="text/javascript">
var TOP = "http://gyazz.com";
var name = "#{name}";

function createXmlHttp(){
    if (window.ActiveXObject) {
        return new ActiveXObject("Microsoft.XMLHTTP");
    } else if (window.XMLHttpRequest) {
        return new XMLHttpRequest();
    } else {
        return null;
    }
}

var attr = [];

function sendattr(){
  file = TOP + "/programs/setattr.cgi?name=" + encodeURIComponent(name) + "&protected=" + attr['protected'];
  xmlhttp = createXmlHttp();
  xmlhttp.open("GET", file , true);
  xmlhttp.send("");
//  alert(event.target.checked);
//  alert(protected.checked);
}

function setattr(event){
  attr[event.target.id] = event.target.checked;
  sendattr();
}

var checkbox_protected = document.getElementById('protected');
checkbox_protected.addEventListener("change", setattr, false);
checkbox_protected.checked = #{attr['protected'] == 'true' ? 'true' : 'false'};

</script>
EOF
    }
  }
}
