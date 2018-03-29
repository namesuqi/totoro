#!/usr/bin/python
# coding:utf-8
# Author=JKZ
# get isp and province by ip

import urllib2
import json

url = 'http://ip.taobao.com/service/getIpInfo.php?ip='
# url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip='


def checkTaobaoIP(ip):
    try:
        response = urllib2.urlopen(url + ip, timeout=5)
        result = response.readlines()
        data = json.loads(result[0])
        return "%15s: %s-%s-%s" % (ip, data['data']['isp'], data['data']['region'], data['data']['city'])
    except:
        return "%15s: timeout" % ip

if __name__ == "__main__":
    # f = open('ip.txt')
    # ips = f.readlines()
    # f.close()
    #
    # f = open('ip-check.txt', 'w')
    # for ip in ips:
    #     line = checkTaobaoIP(ip.strip())
    #     if line:
    #         print line.encode('utf-8')
    #         f.write(line.encode('utf-8')+'\n')
    #     else:
    #         print line
    #         f.write(line+'\n')
    # f.close()
    # print "Done!"
    print checkTaobaoIP("1.119.132.114")
