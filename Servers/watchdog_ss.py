import os
import re
import urllib.request
import socks
import socket
import json
import time

# /home/xuwei/git/anproxygo/anproxygo -c glxwgg.tpddns.cn:6777 -p 192.168.10.34:1080 -t c
def KillClient():
    os.system("taskkill /F /IM shadowsocks2-win64.exe")
def _CheckNet():
    # 设置SOCKS5代理
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 6080)
    socket.socket = socks.socksocket
    # 发送请求
    response = urllib.request.urlopen("http://ip-api.com/json", timeout=30)
    json_str = response.read().decode('utf-8')
    data = json.loads(json_str)
    if 'query' in data :
        return True
    return False
def CheckNet():
    ret = False
    try:
        ret=_CheckNet()
    except Exception as e:
        print(e)
        ret = False
    return ret

# Check()
check_count =0
def mainloop():
    global check_count
    if CheckNet():
        check_count  =  0
    else :
        check_count  =  check_count +1
    if check_count > 6:
        KillClient()
        check_count = 0
    time.sleep(100)


while True:
    try:
        mainloop()
    except Exception as e:
        check_count  =  check_count +1
        print(e)
        time.sleep(100)