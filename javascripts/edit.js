//
// $Date: 2005-11-28 15:02:58 +0900 (Mon, 28 Nov 2005) $
//

var timeout;

var TOP = "http://gyazz.com"

document.onkeyup = keyup;

function keyup(event){
  if(timeout) clearTimeout(timeout);
  timeout = setTimeout("writedata()",2000);

  // 書き込みが必要な状態になると背景を黄色くしていたが、
  // ウザい気もするのでやめてみる。
  //var input = document.getElementById("contents");
  //input.style.backgroundColor = "#ffff80";
}

function createXmlHttp(){
    if (window.ActiveXObject) {
        return new ActiveXObject("Microsoft.XMLHTTP");
    } else if (window.XMLHttpRequest) {
        return new XMLHttpRequest();
    } else {
        return null;
    }
}

function writedata(){
  xmlhttp = createXmlHttp();
  xmlhttp.open("POST", TOP + "/programs/postdata.cgi" , true);
  xmlhttp.setRequestHeader("Content-Type" , "application/x-www-form-urlencoded");
  xmlhttp.setRequestHeader("Content-Type" , "text/html; charset=utf-8"); //2006/11/10追加 for Safari
  var textarea = document.getElementById('contents');
  data = textarea.value;
  postdata = "data=" + encodeURIComponent(name + "\n" + title + "\n" + data);
  xmlhttp.send(postdata);
}
