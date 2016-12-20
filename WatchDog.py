#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author: komi

__author__ = 'komi'

import requests as req
import time
import chardet
from optparse import OptionParser
import hashlib


headers = {
    'User-Agent':'Mozilla/5.3 (Macintosh; U; Intel Mac OS X 9_6_0; en-US) AppleWebKit/53.0 (KHTML, like Gecko) Chrome/4.0.204.0 Safari/532.0',
    'Accept-Encoding': 'gzip, deflate, sdch',
}
# 手动设置http 或 https 等代理
# proxies = {'http':"http://127.0.0.1:8080/", 'https':"https://127.0.0.1:8443/"}

proxies = {}
# 曾经的文件的hash值，用来判断是不是曾经已经取得过.
old_hash = []

# 抓取新文件-重复3次

def update_info(watch_url,retry_times):
    global proxies
    for i in range(retry_times):
        try:
            new_hash = ""
            new_fileText = ""
            newrespon = req.get(url=watch_url,
                         timeout=5,
                         headers=headers,
                         proxies=proxies
            )
            if newrespon.status_code == 200 or len(newrespon.content) > 2:
                md5 = hashlib.md5()
                new_fileText = newrespon.content
                md5.update(new_fileText)
                new_hash = md5.hexdigest()
                return new_hash, new_fileText
            else:
                time.sleep(1)
                continue
        except Exception, e:
            time.sleep(1)
            continue
    # 3次更新文件均失败
    return None, None


# 写入文件

def write_file(fileText, fileName):
    try:
        print u'[+]--------发现更新-----------[+]'
        fp = open(fileName, "wb")
        charset = chardet.detect(fileText)['encoding']
        if charset != "utf-8":
            fileText = fileText.decode("GBK", 'ignore').encode('utf-8')
        fp.write(fileText)
        fp.close()
        print u'[+]--------新文件为:'+fileName+u'-------[+]'

        return True
    except Exception,e:
        print u"[+]Can't Create New File Or Permission denied "
        return False

# WatchDog

def WatchDog(watch_url, timesleep, retry_times):
    TIMESLEEP = timesleep
    while True:
        now_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        new_hash, new_fileText = update_info(watch_url=watch_url,retry_times = retry_times)

        if new_hash and new_fileText and new_hash not in old_hash:
            write_flag = write_file(fileText=new_fileText, fileName=now_time+".txt")
            old_hash.append(new_hash)
        elif not new_hash or not new_fileText:
            print "URL Wrong!!"

        print u"[+]+++++本轮采集完成时间: " + now_time + u"+++++[+]"

        time.sleep(timesleep)


# 入口函数
if __name__ == '__main__':
    print u'''[+]+++++++++++++++++++++++++++++++++++++++++++++++[+]
[+]++++++++++++++++文件采集Tool+++++++++++++++++++[+]
[+]+++++++++++++++++++++++++++++++++++++++++++++++[+]
    '''
    watch_url = "https://www.baidu.com/robots.txt"
    timesleep = 60
    retry_times = 3
    parser = OptionParser(usage='''usage: python %prog -U http://xxx.xxx.xxx.xxx/test.txt -T 300''')

    parser.add_option('-U', '--url', default=False, dest="url", help='the url your want to watch.')
    parser.add_option('-T', '--timesleep', default=60, dest="timesleep", help='the time to sleep before next check.')
    parser.add_option('-R', '--retry_times', default=3, dest="retry_times", help='retry times when update file fail.')

    (options, args) = parser.parse_args()

    if options.url:
        watch_url = options.url
        if options.timesleep:
            timesleep = options.timesleep
        if options.retry_times:
            retry_times = options.retry_times

        WatchDog(watch_url=watch_url, timesleep=float(timesleep), retry_times=int(retry_times))
    else:
        parser.print_help()
        exit(0)