#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: CF_HB
# CreatedTime: 2016-07-15
# 说明:
# 一个免费Shadowsocks提供网站自动更新密码的脚本
#

import requests
import json

SHADOWSOCKS_URL = 'http://www.ishadowsocks.com/'


def findPassword(content, type):
    passStr = ''

    if 'A' == type:
        passStr = u"A密码"
    elif 'B' == type:
        passStr = u'B密码'
    elif 'C' == type:
        passStr = u"C密码"
    index = content.index(passStr)

    # 格式:A密码：xxxxxxxx
    password = content[index + 4:index + 12]

    return password


def updateConfigFile(passwordList):
    # 从模板文件复制
    dst = 'gui-config.json'
    print "[+] connecting  successfull..."
    # 修改模板文件
    f = open(dst, mode='r+')
    data = f.read()
    decoded = json.loads(data)
    configs = decoded['configs']
    print "[+] set new passwords..."

    for cfg in configs:
        if cfg['server'] == "US1.ISS.TF":
            cfg['password'] = passwordList[0]
            continue
        if cfg['server'] == "HK2.ISS.TF":
            cfg['password'] = passwordList[1]
            continue
        if cfg['server'] == "JP3.ISS.TF":
            cfg['password'] = passwordList[2]
            continue

    # 先清空文件
    f.seek(0,0)
    f.truncate()
    f.flush()

    # 再写入文件
    f.write(json.dumps(decoded).decode("unicode_escape").encode("utf-8"))
    f.flush()
    f.close()
    print "[+] Congratulations, All Done..."


if __name__ == '__main__':
    print "[+] updating passwords..."
    dst = 'gui-config.json'
    # 修改模板文件
    typeList = ['A', 'B', 'C']
    passwordList = []
    try:
        print "[+] connecting ..."
        content = requests.get(SHADOWSOCKS_URL, timeout=5).content.decode('utf-8')
        for type in typeList:
            passwordList.append(findPassword(content, type))
        updateConfigFile(passwordList)
    except Exception,e:
        print "[Error] connect failed ..."
        print "[+]check your network is good?"
