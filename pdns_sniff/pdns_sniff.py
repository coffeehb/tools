#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/2/5 上午9:59
# @Author  : Komi
# @File    : pdns_sniff.py
# @Ver:    : 0.1

from gevent import monkey;monkey.patch_all()
import gevent
from scapy.all import sr1, IP, UDP, DNS, DNSQR, DNSRR
from scapy.all import sniff
import datetime
import argparse
import MySQLdb as mysql
import Queue
import time
import traceback

dnslogsQueueList = Queue.Queue()
hook_domains = ['baidu.com']

def save_mysql():
    print "[+] Start Saving......"
    global dnslogsQueueList
    # save all the times.
    while True:

        try:
            conn = mysql.connect(user='root', passwd='yourpassword', host='127.0.0.1', db='dnslogsDB')
            cur = conn.cursor()
        except mysql.Error, e:
            print '\033[91m' + '\033[1m' + '[+].... Login mysql failed,check your config ....[+]' + '\033[0m'

        while not dnslogsQueueList.empty():
            try:
                record_log = dnslogsQueueList.get()

                domain = record_log['domain']
                domain_ip = record_log['domain_ip']
                dns_client_ip = record_log['dns_client_ip']
                dns_server_ip = record_log['dns_server_ip']
                record_time = record_log['record_time']

                try:
                    pam = (domain, domain_ip, dns_client_ip, dns_server_ip, record_time)
                    sql = "insert into dnslogs (`domain`, `domain_ip`, `dns_client_ip`, `dns_server_ip`, `record_time`) values(%s,%s,%s,%s,%s)"
                    cur.execute(sql, pam)
                    conn.commit()
                except Exception,e:
                    print '\033[91m' + '\033[1m' + '[+].... Save failed check your mysql status....[+]' + '\033[0m'
                    time.sleep(10)
            except:
                print "[!]write file fails."
        time.sleep(5)


def value_sniper(arg1):
    string_it = str(arg1)
    snap_off = string_it.split('=')
    working_value = snap_off[1]
    return working_value[1:-1]


def packetHandler(a):
    global dnslogsQueueList
    global hook_domains

    for pkt in a:  # read the packet
        if pkt.haslayer(DNSRR):  ## Read in a pcap and parse out the DNSRR Layer
            domain1 = pkt[DNSRR].rrname  # this is the response, it is assumed

            if domain1 != '':  # ignore empty and failures
                domain = domain1[:-1]
                # Check if the domain is what I want
                flag = False
                for temp in hook_domains:
                    if temp in domain:
                        flag = True
                if not flag:
                    continue

                record_log = {}

                pkt_type = pkt[DNSRR].type  # identify the response record that requires parsing

                # date/time
                time_raw = pkt.time  # convert from unix to 8 digit date
                pkt_date = (datetime.datetime.fromtimestamp(int(time_raw)).strftime('%Y%m%d %H:%M:%S'))
                record_log['record_time'] = str(pkt_date)

                dns_server = pkt[IP].src  # dns_server
                dns_client = pkt[IP].dst  # dns_client

                record_log['dns_client_ip'] = dns_client
                record_log['dns_server_ip'] = dns_server

                if pkt_type == 2 or pkt_type == 5:  # this should work for type 5 and 2
                    x = pkt[DNSRR].answers
                    dns_strings = str(x)
                    fields = dns_strings.split('|')
                    for each in fields:
                        if 'type=NS' or 'type=A' in each:
                            subeach = str(each)
                            y = subeach.split(' ')  # split lines
                            for subsubeach in y:
                                if 'rdata' in subsubeach:
                                    ipaddress = value_sniper(subsubeach)

                                    if ipaddress != None:
                                        print "[+]domain: " + str(domain), "==>", ipaddress, "[+]"
                                        record_log['domain_ip'] = ipaddress
                                        record_log['domain'] = str(domain)
                                        dnslogsQueueList.put(record_log)

                elif pkt_type == 1 or pkt_type == 12 or pkt_type == 28:  # 32bit IP addresses
                    ipaddress = pkt[DNSRR].rdata
                    print "[+]domain: " + str(domain), "==>", ipaddress, "[+]"

                    record_log['domain_ip'] = ipaddress
                    record_log['domain'] = str(domain)
                    dnslogsQueueList.put(record_log)
                else:
                    print "[+]domain: " + str(domain), "  ==>  ", "NULL", "[+]"
                    record_log['domain_ip'] = "NULL"
                    record_log['domain'] = str(domain)
                    dnslogsQueueList.put(record_log)


def run(interface='en0'):
    print "[+] Start Recording......"
    sniff(iface=interface, filter="udp and port 53", prn=packetHandler)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='PROG', description='Passive Dns collector with scapy.')
    parser.add_argument('-i', '--interface', help='specify the interface name default:en0 ')
    parser.add_argument('-d', '--domains', help='Record the domain name you want eg: baidu.com,tengcent.com')
    args = parser.parse_args()
    interface = "en0"

    if args.interface:
        interface = args.interface
    if args.domains:
        temps = args.domains
        hook_domains = temps.split(",")

    if not args.interface:
        print '\033[99m' + '\033[1m', parser.print_help(), '\033[0m'
        print '\033[95m' + '\033[1m' + 'usage: \n\t1. python pdns_sniff.py -i eth0\n\t2. python pdns_sniff.py -i en0 -d "baidu.com,jd.com,tencent.com"\n''\033[0m',
        exit(-1)

    try:
        gevent.joinall([gevent.spawn(run, interface), gevent.spawn(save_mysql)])
    except Exception,e:
        traceback.print_exc()
