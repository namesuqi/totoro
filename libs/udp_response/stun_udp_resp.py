# coding=utf-8
"""
stun related udp parser

__author__ = 'zengyuetian'

"""

from libs.decorator.trace import *


@print_trace
def parse_stun_rsp_data(rsp_data):
    """
    通过UDP协议解析stun返回的rsp包
    :param rsp_data:
    :return:
    """
    if rsp_data in (None, ""):
        print "Rsp_data is None"
        return None
    elif rsp_data.startswith("8102"):
        step = int(rsp_data[4:6], 16)
        pub_ip_hex = rsp_data[6:14]
        pub_ip = '.'.join([str(int(pub_ip_hex[i:i+2], 16)) for i in xrange(0, len(pub_ip_hex), 2)])
        pub_port = int(rsp_data[14:18], 16)
        return step, pub_port
    elif rsp_data.startswith("8104"):
        rsp_code = int(rsp_data[4:6], 16)
        timestamp = int(rsp_data[6:22], 16)
        return rsp_code
    elif rsp_data.startswith("a102"):
        peer_id = str(rsp_data[4:36]).upper()
        default_str = rsp_data[36:-4]  # default str is contains NAT_TYPE=6, PUBLIC_IP=0.0.0.0, PUBLIC_PORT=0, PRIVATE_IP=0.0.0.0,PRIVATE_PORT=0
        check_sum = rsp_data[-4:]
        return peer_id, default_str, check_sum
    else:
        print "Cannot parse rsp_data : {0}".format(rsp_data)
        return False