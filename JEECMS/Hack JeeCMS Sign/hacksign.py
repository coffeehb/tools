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
            str1 = {'version','timestamp','client','channel','uid','token','settype','nickname','sex','app_name','device_name','device_system_version','mobile','mobilecode','password','passwordOld','passwordNew','uidHome','device','name','id','dynamic_id','comment_id','content','label_id','page','page_size','uid_to','type','has_dynamic','lon','lat','province','city','taskid','openid','accesstoken','loginfrom','uidReceive','num','keyword','flag','posid','uidRival','last_id','addtime','time','tribe_title',"tribe_pwd","tribe_id","tribe_flag","tribe_checktype","tribe_content","tribe_type","tribe_value","tribe_member_ids","tribe_yaoqing_uid","tribe_search_id",'idcard','payChannel','voice_id','voice_info','voice_file','voice_sec','voice_sort','sync','pid','birthday','cardId','cardIds','alipay','code','money','mark','ext',"usercard_sex","usercard_age_range",'emulator','vpn','multi_apk'}
            old_sign = ""
            # defalut appKey
            appKey = "b685e42b1253a1eedcf6431fcc908ea1"

            hash_param = ""
            param_list = body.split("&")

            temp_dict = {}
            for pa in param_list:
                t = pa.split("=",1)
                temp_dict[t[0]] = t[1]

            tmmmm = temp_dict.items()

            tmmmm.sort()
            for (k, v) in tmmmm:
                if k == "sign":
                    old_sign = v
                    print "old sign = ",v
                    continue
                if k in str1:
                    hash_param += "%s=%s&" % (k, v)
            hash_param = (hash_param[:-1])
            hash_param +=   appKey
            sign = hashlib.md5(hash_param).hexdigest()
            print "new sign = ",sign
            return old_sign,sign
        except Exception, e:
            return "",""
