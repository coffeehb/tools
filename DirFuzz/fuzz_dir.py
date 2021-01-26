#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import multiprocessing
import sys
import chardet
from difflib import SequenceMatcher
# 用法
# python fuzz_dir.py fuzz.txt http://d.xiaojukeji.com/admin/ 0 success.txt

# 相似度算法，对比404页面和WAF拦截页面
# https://thief.one/2018/04/12/1/
seqm404 = SequenceMatcher()
seqmWAF = SequenceMatcher()

# 接受的返回状态码
ACESS_CODE = [
    200,201,301,302,305,400,401,403,405,500,503
]

# 无效的404页面
PAGE_404 = [
    'page_404"', "404.png", u'找不到页面', u'文件不存在', u'找不到网页',u'页面出错啦',  u'页面找不到', "Not Found", u"访问的页面不存在",
    "page does't exist", 'notice_404', '404 not found', 'Forbidden', 'Not Implemented'
]
# 页面内容相似度0.5上限，我认为404页面/或被WAF拦截的页面应该是高度相似的。
rat_max = 0.5
GREEN = '\033[0;92m{}\033[0;29m'
OTHER = '\033[0;33m{}\033[0;29m'

base_path = sys.argv[2]
fuzz_dir = sys.argv[1]
is_debug = sys.argv[3]
if len(sys.argv)>4:
    save_file = sys.argv[4]
else:
    save_file = '200.txt'

headers = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
     'Referer': 'https://www.baidu.com',
     'Cookie': 'test_for_securiuty=cfhb2020',
     'Accept-Encoding': "gzip, deflate",
     'Accept-Language': "zh-CN,zh;q=0.9",
     'Connection': "close"
     }
s_list = []
task = multiprocessing.Queue()
mgr = multiprocessing.Manager()
data = mgr.list()

filename = fuzz_dir

count_fuzz = 0

for line in open(filename):
    uri = line.strip()
    if not uri.startswith("/"):
        uri = "/"+uri
    data.append(uri)
    count_fuzz +=1

print(GREEN.format('{}'.format(str(count_fuzz))))


def checkdir(url, timeout=3):
    try:
        r = requests.get(url, headers=headers, timeout=timeout, verify=True, allow_redirects=True)
        status_code = r.status_code
        coding = chardet.detect(r.content[:10000]).get('encoding')
        text = r.content[:20000].decode(coding)
        return status_code, text
    except Exception as e:
        # print(e)
        status_code = 404
        text = ""
    return status_code, text

def make_url(uri,timeout=3):
    global s_list
    global PAGE_404
    global ACESS_CODE
    global rat_max

    if base_path.endswith("/"):
        url = base_path[:-1] + uri
    else:
        url = base_path + uri

    s_code, text = checkdir(url,timeout=timeout)
    seqm404.set_seq2(text)
    seqmWAF.set_seq2(text)

    rat404 = seqm404.ratio()
    ratwaf = seqmWAF.ratio()
    # print (ratwaf)
    # print (rat404)
    # 和 404 及 WAF触发时返回内容相似度大于70%，判定为不健康页面。
    if rat404 > rat_max or ratwaf > rat_max:
        is_health = False
    else:
        is_health = True
    # print (text)
    for CODE in PAGE_404:
        if CODE.lower() in text.lower():
            is_health = False
            if is_debug == "1":
                msg = "[%s] %s " % (url, "s")
                print(OTHER.format('{}'.format(msg)))
            break

    msg = "[%s] %s " % (s_code, url)
    if s_code in ACESS_CODE and is_health:
        # s_list.append(msg)
        print(GREEN.format('{}'.format(msg)))
        with open(save_file, "a+") as wf:
            wf.write('{}\n'.format(msg))
    else:
        if is_debug == "1":
            print(OTHER.format('{}'.format(msg)))
    return text

def work():
    start = time.time()
    p = multiprocessing.Pool(20)
    p.map_async(make_url, data)
    p.close()
    p.join()
    print(OTHER.format('\nspend times :{} \n'.format(str(time.time()-start))))


def output():
    print ("xxx - xxx" * 33)
    global s_list
    print (len(s_list))
    for url in s_list:
        with open(save_file, "a+") as wf:
            wf.write('{}\n'.format(url))


if __name__ == '__main__':

    temp404Text = make_url(uri="/AreYouKidingMe", timeout=8)
    seqm404.set_seq1(temp404Text)

    tempWAFText = make_url(uri="/index.php?text=<script>alert(/xss/)</script>", timeout=8)
    seqmWAF.set_seq1(tempWAFText)
    try:
        work()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        # output()

