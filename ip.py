from gevent import monkey;monkey.patch_all()
import gevent
import requesocks as requests
import json
import sys
import Queue

ipQueueList = Queue.Queue()

def readfile(fname=sys.argv[1]):
	c = 0
	with open(fname,'r') as rf:
		for line in rf.readlines():
			c +=1
			ipQueueList.put(line[:-1].strip())

	print "[*]--FOUND %s IPS--[*]" % str(c)
def run():
	global ipQueueList
	while not ipQueueList.empty():

		ip = ipQueueList.get()
		burp0_url = "https://www.virustotal.com:443/ui/ip_addresses/%s/resolutions?cursor=&limit=10" % ip
		burp0_headers = {"Accept": "*/*", "Accept-Language": "en", "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)", "Connection": "close"}
		proxies = {"http": "socks5://127.0.0.1:9000","https": "socks5://127.0.0.1:9000"}
		session = requests.session()
		session.proxies = proxies
		session.headers = burp0_headers
		resp = session.get(burp0_url, timeout=20).content
		try:
			msg =  json.loads(resp)['data'][0]['attributes']['host_name']
		except:
			try:
				print json.loads(resp)['data']
			except Exception as e:
				msg = "NotFoundError"
		finally:
			print "[+]%s ====>>> %s" % (ip, msg)

if __name__ == '__main__':
	readfile(sys.argv[1])
	gevent.joinall([gevent.spawn(run) for i in range(0, 3)])
