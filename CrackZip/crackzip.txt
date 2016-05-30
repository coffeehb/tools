
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         Zip File Password Freak
# Purpose:      You know that ;)
#
# Author:      Osanda Malith Jayathissa
#
# E-Mail:       OsandaJayathiss@gmail.com
# Website:      http://osandamalith.wordpress.com
# Twitter:      @OsandaMalith
# Created:     14/12/2013
# Copyright:   (c) Osanda 2013
# Licence:     Open Source
# /!\ Use this for educational purposes only.
#-------------------------------------------------------------------------------

import zipfile, os
import optparse
from threading import Thread

def extractFile(z, password):
        try:
                z.extractall(pwd=password)
                print '[+] Found password ' + password + '\n'
        except:
                pass
def banner():
        print """


d8888888P oo              88888888b oo dP
     .d8'                 88           88
   .d8'   dP 88d888b.    a88aaaa    dP 88 .d8888b.
 .d8'     88 88'  `88     88        88 88 88ooood8
d8'       88 88.  .88     88        88 88 88.  ...
Y8888888P dP 88Y888P'     dP        dP dP `88888P'
             88
             dP

        88888888b                            dP
        88                                   88
        a88aaaa    88d888b. .d8888b. .d8888b. 88  .dP
        88        88'  `88 88ooood8 88'  `88 88888"
        88        88       88.  ... 88.  .88 88  `8b.
        dP        dP       `88888P' `88888P8 dP   `YP


[+] Coded by Osanda Malith Jayathissa
[+] E-Mail: OsandaJayathissa@gmail.com
[+] Website: osandamalith.wordpress.com

        """

def main():
        banner()
        os.system('color 0a')
        parser = optparse.OptionParser("%prog "+"-f <zipfile>,\
 -d <dictionary>")
        parser.add_option('-f', dest='fname', type='string',\
        help='Your zip file to be cracked')
        parser.add_option('-d', dest='dname', type='string',\
        help='Your dictionary file')
        (options, args) = parser.parse_args()
        if (options.fname == None) | (options.dname == None):
                print parser.usage
                exit(0)
        else:
                zname = options.fname
                dname = options.dname

        zfile = zipfile.ZipFile(zname)
        info =  zipfile.ZipInfo(zname)
        info =  info.filename
        print '[~] Cracking Password for ' + info+ '\n'
        passFile = open(dname)
        for line in passFile.readlines():
                password = line.strip('\n')
                t = Thread(target=extractFile, args=(zfile, password))
                t.start()

if __name__ == '__main__':
        main()
