from burp import IBurpExtender
from burp import IHttpListener
from java.io import PrintWriter
import os

cookie_txt = 'cookie.txt'

file_path = os.getcwd() + os.sep + cookie_txt
print "CookieXSS Code By Nerd."

msg = """Write Your Cookie into file: %s \nLike:\ndomain=baidu.com\nbid=c5/a==; BaiLoginName=test;SessionID=F21DFEWFAFFAFQFQEFAFAEF;""" % file_path
print msg

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):

        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Cookie Via XSS")
        callbacks.registerHttpListener(self)
        self.stdout = PrintWriter(callbacks.getStdout(), True)
        self.stderr = PrintWriter(callbacks.getStderr(), True)
        callbacks.issueAlert("Loaded Successfull.")

    def processHttpMessage(self, toolFlag, messageIsRequest, currentRequest):
        if messageIsRequest:

            requestInfo = self._helpers.analyzeRequest(currentRequest)

            self.headers = list(requestInfo.getHeaders())
            # self.setHeader('Cookie',"Cookie_HelloMe")
            cookie_text = ""
            hook_host = requestInfo.getUrl().getHost()

            if os.path.exists(file_path):
                with open(file_path, 'r') as rf:
                    cooki_domain = rf.readline().replace("\n","").split("=")[1]

                    if str(cooki_domain) in str(hook_host):
                        for line in rf.readlines():
                            cookie_text += line.replace("\n","")
            else:
                pass

            if len(cookie_text) > 10:
                self.stdout.println("[+]-------Hack Inject Cookie-------[+]")

                self.stdout.println(cookie_text)
                self.setHeader('Cookie',cookie_text)

            bodyBytes = currentRequest.getRequest()[requestInfo.getBodyOffset():]
            self.body = self._helpers.bytesToString(bodyBytes)

            newMessage = self._helpers.buildHttpMessage(self.headers, self.body)
            currentRequest.setRequest(newMessage)

        # Process responses
        else:
            pass

    def setHeader(self, header, value):
        new_headers = []
        for h in self.headers:
         if header in h:
          h = header + ': ' + value
         new_headers.append(h)
        self.headers = new_headers
