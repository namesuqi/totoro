# coding=utf-8
# common constants
TS_IP = "172.30.0.18"
TS_PORT = "9510"

HEADERS = {
   "Accept": "application/json",
   "Content-Type": "application/json",
   "Connection": "close",
   # "User-Agent": "YunshangSDK/3.19.9"
}

FILE_ID_NOT_EXIST = "1445FA4CB89E4DA5BDD8BD749DDEB082"  # not exist
FILE_ID_EXIST = "504FE07AA1824A9D92B170BE316A1A3C"  # exist

SDK_FILE_STATUS_LIST = ["downloading", "interrupt", "done", "none"]

DEFAULT_VERSION = "4.0.10"
DEFAULT_NAT_TYPE = 4
DEFAULT_PUBLIC_IP = "59.63.166.73"  # isp: 100017
# 100017: 116.231.59.29, 100026: 110.16.0.0, 000000: 112.13.0.0
DEFAULT_PUBLIC_PORT = 12345
DEFAULT_PRIVATE_IP = "192.168.2.22"
DEFAULT_PRIVATE_PORT = 11111
DEFAULT_STUN_IP = "192.168.1.202"
DEFAULT_MACS = {"name": "eno16777736", "addr": "00:0C:29:AE:1C:49"}
