# 利用scapy 造了一个Passive DNS Collector 工具——pdns_sniff

### pdns_sniff是什么？

简单理解为一个记录你发起过的DNS请求的东西，利用了Passive DNS 思路，被动的记录发起过的DNS请求。

### pdns_sniff有什么用？

利用这样的工具可以帮助我在愉快的上网的同时，轻松搜集到测试目标的各种子域名。

### pdns_sniff原理是什么？

利用了python里的强大的scapy套件，运用它抓取，解析出DNS请求包从而得到各种域名。使用了mysql进行数据存储，利用了gevent协程进行并发进行数据包的分析和写入数据库（PS：刚学gevent，拿来用用。）

### 效果图

效果图一：数据库中记录1
![数据库中记录1](http://www.coffeehb.cn/zb_users/upload/2017/02/20170205223502148630530254796.png "数据库中记录1")

效果图二：数据库中记录2
![数据库中记录2](http://www.coffeehb.cn/zb_users/upload/2017/02/20170205223524148630532412525.png "数据库中记录2")

效果图三：工具输出记录
![工具输出记录](http://www.coffeehb.cn/zb_users/upload/2017/02/20170205223538148630533859265.png "工具输出记录")

效果图四：使用方法
![使用方法](http://www.coffeehb.cn/zb_users/upload/2017/02/20170205223434148630527450376.jpeg "使用方法")

### 需要安装的三方库

1.  gevent
2.  scapy
3.  MySQLdb

### 需要修改的数据库配置

`大概在第29行
conn = mysql.connect(user='root', passwd='yourpassword', host='127.0.0.1', db='dnslogsDB')`

### pdns_sniff的相关代码
[pdns_sniff代码](https://github.com/coffeehb/tools/pdns_sniff)

### 欢迎交流

QQ: 759601966

