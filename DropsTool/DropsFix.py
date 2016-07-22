import argparse
import os
import requests as req
import threading
import re
import Queue
import hashlib
# Name : A Repair Tool For Static Resource
# Author      : CF_HB
# Date        : 2016/07/22
# usage: python DropsFix.py -p "D:\\drops_html" -n 20

target_html_list = []
target_html_queue = Queue.Queue()


def GetHtmlList(level, path):
    dirList = []
    global target_html_list
    files = os.listdir(path)
    dirList.append(str(level))
    for f in files:
        if(os.path.isdir(path + '/' + f)):
            if(f[0] == '.'):
                pass
            else:
                dirList.append(f)
        if(os.path.isfile(path + '/' + f)):
            target_html_list.append(f)
    i_dl = 0

    for dl in dirList:
        if(i_dl == 0):
            i_dl = i_dl + 1
        else:
            # print '-' * (int(dirList[0])), dl
            GetHtmlList((int(dirList[0]) + 1), path + '/' + dl)


def GetHtmlFile(self):
    return ""

class ImageFixThread(threading.Thread):
    def __init__(self, basepath):
        threading.Thread.__init__(self)
        self.dropshtmlpath = basepath

    def run(self):
        while True:
            try:
                if target_html_queue.empty():
                    break
                html_file_path = target_html_queue.get()
                if ".html" not in html_file_path:
                    continue

                # read
                print "[+]Deal "+html_file_path
                html_text = self.ReadFile(self.dropshtmlpath+"//"+html_file_path)
                # pickup
                pic_list = self.ExtractImages(html_text)
                print "[+] Have "+str(len(pic_list))+" images"
                for picurl  in pic_list:
                    name = hashlib.md5(picurl).hexdigest()
                    realpath = self.dropshtmlpath+"//pics//"+name+".jpg"
                    relativepath = "pics/"+name+".jpg"
                    # Save Image
                    imagecontent = self.DownPics(picurl)
                    wf = self.WriteFile(realpath=realpath, filecontent=imagecontent)
                    # Replace url
                    html_text = html_text.replace(picurl, relativepath)
                # Save html file
                flag = self.WriteFile(realpath=self.dropshtmlpath+"//"+html_file_path, filecontent=html_text)
            except Exception , e:
                continue
    def ExtractImages(self,webContent):
        extList = ['m4u','m3u','mid','wma','flv','3g2','mkv','3gp','mp4','mov','avi','asf','mpeg','vob','mpg','wmv','fla','swf','wav','mp3','qcow2','vdi','vmdk','vmx','gpg','aes','ARC','PAQ','tar.bz2','tbk','bak','tar','tgz','gz','7z','rar','zip','djv','djvu','svg','bmp','png','gif','raw','cgm','jpeg','jpg','tif','tiff','NEF','psd','cmd','bat','sh','class','jar','java','rb','asp','cs','brd','sch','dch','dip','pl','vbs','vb','js','asm','pas','cpp','php','ldf','mdf','ibd','MYI','MYD','frm','odb','dbf','db','mdb','sql','SQLITEDB','SQLITE3','asc','lay6','lay','ms11','sldm','sldx','ppsm','ppsx','ppam','docb','mml','sxm','otg','odg','uop','potx','potm','pptx','pptm','std','sxd','pot','pps','sti','sxi','otp','odp','wb2','wks','wk1','xltx','xltm','xlsx','xlsm','xlsb','slk','xlw','xlt','xlm','xlc','dif','stc','sxc','ots','ods','hwp','dotm','dotx','docm','docx','DOT','3dm','max','3ds','xml','txt','CSV','uot','RTF','pdf','XLS','PPT','stw','sxw','ott','odt','DOC','pem','p12','csr','crt','key']
        images_url = []
        for ext in extList:
            imgs = re.findall('http://static.wooyun.org[^<][^>]+?.'+ext, webContent)
            images_url = images_url + imgs
        return images_url

    def DownPics(self, picurl):
        imgcontent = ""
        web = req.get(picurl, timeout=5)
        if web.status_code == 404:
            pass
        else:
            imgcontent = web.content
        return imgcontent

    def ReadFile(self, absolutepath):
        print "[+] Read file"+absolutepath
        filecontent = ""
        try:
            fw = open(unicode(absolutepath, "GBK"), 'r')
            filecontent = fw.read()
            fw.close()
            return filecontent
        except Exception , e:
            print "[error]"+"read error.."
            print e
            fw.close()
            return ""

    def WriteFile(self, realpath, filecontent):
        try:
            print "[+]write: "+realpath
            fw = open(realpath, 'wb')
            fw.write(filecontent)
            fw.flush()
            fw.close()
            return True
        except Exception:
            print "[error]"+"write error.."
            fw.close()
            return False

def run(basepath, count):
    for target_html in target_html_list:
            target_html_queue.put(target_html)
    try:
        os.makedirs(basepath+"//pics")
        print "[+] Create pics success..."
    except:
        print "[+] Create fail..."

    for k in range(int(count)):
        print "[+] start thread " + str(k)
        dt = ImageFixThread(basepath)
        # dt.setDaemon(True)
        dt.setName("DownloadThreadId :"+str(k))
        dt.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', help='the html path.')
    parser.add_argument('-n', help='the thread number.Default:10')
    args = parser.parse_args()
    args_dict = args.__dict__
    path = args_dict['p']
    count = args_dict['n']
    print "[+] Welcome to htmlFixer."
    print "[+] Loading your html files.."
    # path = "D:\\drops"
    # count = 1
    GetHtmlList(1, path)
    if len(target_html_list)>0:
        print "[+] Load successfully.."
        print "[+] Load "+str(len(target_html_list))+" files.."
    else:
        print "[+] Load Fail.."
        exit(0)
    run(path, count)
