#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from burp import IBurpExtender
from burp import IHttpListener
from java.io import PrintWriter
import hashlib
import urllib

print("Hack Sign is working.")

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):

        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Hack Sign With XiaoBU")
        callbacks.registerHttpListener(self)
        self.stdout = PrintWriter(callbacks.getStdout(), True)
        self.stderr = PrintWriter(callbacks.getStderr(), True)
        callbacks.issueAlert("Loaded Successfull.")

    def processHttpMessage(self, toolFlag, messageIsRequest, currentRequest):

        if messageIsRequest:
            requestInfo = self._helpers.analyzeRequest(currentRequest)
            self.headers = list(requestInfo.getHeaders())
            self.host = requestInfo.getUrl().getHost()
            host_sites = ['ortc-signal-cn.heytapmobi.com', '10.13.30.163']
            if self.host not in host_sites:
                return
            print (requestInfo.getUrl().getQuery())
            paraList = requestInfo.getParameters()
            for para in paraList:
                k = para.getName()
                v = para.getValue()
                if k == "timestamp":
                    self.timestamp = v
                if k == "sign":
                    self.old_sign = v
            self.key = "3371f7490d5c4cd5ab00158cb8d86529"
            import time
            tmp = time.time()
            timestamp = str(int(tmp))+"000"
            hash_param = self.key+timestamp+self.key
            sign = hashlib.md5(hash_param).hexdigest()
            new_requestInfo = currentRequest.getRequest()
            for para in paraList:
                # print ("para.getType() == ", para.getType())
                # 0  参数来自URL中
                # 6 参数来自BODY中
                if para.getType() == 0 and 'sign' == para.getName():
                    value = sign
                    key = para.getName()
                elif para.getType() == 0 and 'timestamp' == para.getName():
                    value = timestamp
                    key = para.getName()
                else:
                    value = para.getValue()
                    key = para.getName()
                print("%s === > %s " % (key, value))
                if para.getType() == 0 :
                    newPara = self._helpers.buildParameter(key, value, para.getType())
                    new_requestInfo = self._helpers.updateParameter(new_requestInfo, newPara)

            currentRequest.setRequest(new_requestInfo)

        # Process responses
        else:
            pass
