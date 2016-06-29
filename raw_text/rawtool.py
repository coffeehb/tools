#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'CF_HB'
# 造一个处理Raw格式的文件的库

import re

class RawTool():
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.Host = ""
        self.Content_Length = 0
        self.User_Agent = ""
        self.Content_Type = ""
        self.Cookie = ""
        self.post_data = ""

    # this function come from sqlmap
    def extractRegexResult(self, regex, content, flags=0):
        retVal = None
        if regex and content and "?P<result>" in regex:
            match = re.search(regex, content, flags)
            if match:
                retVal = match.group("result")
        return retVal
    # Return : HOST
    def getHost(self,):
        return self.extractRegexResult(r"Host: (?P<result>.+?)\n", self.raw_text, re.I)
    # Return : Method(POST/GET/PUT..)
    def getMethod(self):
        return self.raw_text[0:self.raw_text.index(" ")]
    # Return : Path
    def getPath(self):
        return self.extractRegexResult(r" (?P<result>.+?) HTTP/1.1", self.raw_text, re.I)
    # Return : Referer
    def getReferer(self):
        return self.extractRegexResult(r"referer: (?P<result>.+?)\n", self.raw_text, re.I)
    # Return : User-Agent
    def getUserAgent(self):
        return self.extractRegexResult(r"User-Agent: (?P<result>.+?)\n", self.raw_text, re.I)
    # Return : Cookie
    def getCookie(self):
        return self.extractRegexResult(r"COOKIE: (?P<result>.+?)\n", self.raw_text, re.I)
    # Return : PostData
    def getPostData(self):
        return self.extractRegexResult(r"\n\n(?P<result>.+?)\n\n", self.raw_text, re.I)
