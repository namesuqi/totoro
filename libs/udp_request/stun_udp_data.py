# coding=utf-8
"""
Prepare data for sending udp messages to stun, YSSTUN
C_DISTINGUISH_STUNv1  = 0x81
C_STUN_QUERY_TYPE_REQ = 1
C_STUN_QUERY_TYPE_RSP = 2
C_STUN_NAT_UPDATE_REQ = 3
C_STUN_NAT_UPDATE_RSP = 4
C_STUN_NAT_QUIT       = 5

__author__ = 'zsw'

"""
import socket
import struct
import time
import binascii
from libs.decorator.trace import *


@print_trace
def query_type_req_data(step, udp_check):
    """
    sdk => stun
    :param step: 1byte, 1 or 2, 目的端口为9000, 则为1, 目的端口为9002, 则为2
    :param udp_check: 是否包含checksum
    :return:
    """
    step = str(step).rjust(2, '0')
    data_combine = "8101{0}".format(step).ljust(6, '0')
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def query_type_req_data_indefinite(step, udp_check):
    """
    sdk => stun 报文长度不定
    :param step: 1byte, 1 or 2, 目的端口为9000, 则为1, 目的端口为9002, 则为2
    :param udp_check: 是否包含checksum
    :return:
    """
    step = str(step)
    if len(step) % 2 != 0:
        step += '0'
    data_combine = "8101{0}".format(step)
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def query_type_rsp_data(pub_ip, pub_port, step, udp_check):
    """
    stun => sdk
    :param pub_ip: 4bytes, sdk的公网地址
    :param pub_port: 2bytes, sdk的公网port
    :param step: 1byte
    :param udp_check: 是否包含checksum
    :return:
    """
    step = str(step).rjust(2, '0')
    pub_ip_split = pub_ip.split(".")
    pub_ip_hex = ""
    for i in pub_ip_split:
        # 将IP按"."分隔并转换成十六进制，从右侧数起不足2个字符串时用0填充
        i_hex = str(hex(int(i))[2:]).rjust(2, '0')
        pub_ip_hex += i_hex
    # 将SDK公网IP转换成十六进制，从右侧数起不足4个字符串时用0填充
    pub_port_hex = str(hex(int(pub_port)))[2:].rjust(4, '0')
    data_combine = "8102{0}{1}{2}".format(step, pub_ip_hex, pub_port_hex).ljust(18, '0')
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def nat_update_req_data(peer_id, nat_type, pri_ip, pri_port, udp_check):
    """
    sdk => stun
    :param peer_id: 16bytes, sdk的peer_id
    :param nat_type: 1byte, sdk自己探测出来的NAT类型
    :param pri_ip: 4bytes, sdk的私网IP
    :param pri_port: 2bytes, sdk的私网port
    :param udp_check: 是否包含checksum
    :return:
    """
    peer_id = str(peer_id.lower()).rjust(32, '0')
    nat_type = str(nat_type).rjust(2, '0')
    pri_ip_split = pri_ip.split(".")
    pri_ip_hex = ""
    for i in pri_ip_split:
        i_hex = str(hex(int(i))[2:]).rjust(2, '0')
        pri_ip_hex += i_hex
    pri_port_hex = str(hex(int(pri_port)))[2:].rjust(4, '0')
    data_combine = "8103{0}{1}{2}{3}".format(peer_id, nat_type, pri_ip_hex, pri_port_hex).ljust(50, '0')
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def nat_update_req_data_indefinite(peer_id, nat_type, pri_ip, pri_port, udp_check):
    """
    sdk => stun 报文长度不定
    :param peer_id: 16bytes, sdk的peer_id
    :param nat_type: 4bytes, sdk自己探测出来的NAT类型
    :param pri_ip: 4bytes, sdk的私网IP
    :param pri_port: 2bytes, sdk的私网port
    :param udp_check: 是否包含checksum
    :return:
    """
    peer_id = str(peer_id.lower())
    nat_type = str(nat_type).rjust(2, '0')
    pri_ip_split = pri_ip.split(".")
    pri_ip_hex = ""
    for i in pri_ip_split:
        i_hex = str(hex(int(i))[2:]).rjust(2, '0')
        pri_ip_hex += i_hex
    pri_port_hex = str(hex(int(pri_port)))[2:]
    data_combine = "8103{0}{1}{2}{3}".format(peer_id, nat_type, pri_ip_hex, pri_port_hex)
    if len(data_combine) % 2 != 0:
        data_combine += '0'

    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def nat_update_rsp_data(rsp_code, udp_check):
    """
    stun => sdk
    :param rsp_code: 1byte, 状态码; timestamp, 8bytes
    :param udp_check: 是否包含checksum
    :return:
    """
    rsp_code = str(rsp_code).rjust(2, "0")
    timestamp = int(time.time()*1000)
    timestamp_hex = str(hex(timestamp))[2:-1].rjust(16, '0')
    data_combine = "8104{0}{1}".format(rsp_code, timestamp_hex)
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def nat_quit_data(peer_id, udp_check):
    """
    sdk => stun
    :param peer_id: 16bytes, sdk的peer_id
    :param udp_check: 是否包含checksum
    :return:
    """
    peer_id = str(peer_id.lower()).rjust(32, '0')
    data_combine = "8105{0}".format(peer_id)
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def nat_quit_data_indefinite(peer_id, udp_check):
    """
    sdk => stun 报文长度不定
    :param peer_id: 16bytes, sdk的peer_id
    :param udp_check: 是否包含checksum
    :return:
    """
    peer_id = str(peer_id.lower())
    data_combine = "8105{0}".format(peer_id)
    if len(data_combine) % 2 != 0:
        data_combine += '0'
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def rrpc_ack_data(uuid, peer_id, result, udp_check):
    """

    :param uuid: 16bytes, 报文唯一标识
    :param peer_id: 16bytes, sdk的peer_id
    :param result:
    :param udp_check: 是否包含checksum
    :return:
    """
    distinguish = '91'
    token = str(uuid).rjust(32, '0')
    reserved = '0' * 64
    rrpc_id = '0' * 4
    peer_id = str(peer_id.lower()).rjust(32, '0')
    result = str(result).rjust(2, '0')
    data_combine = distinguish + token + reserved + rrpc_id + peer_id + result
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def rrpc_join_leifeng_data(uuid, peer_id, file_id, file_url, piece_size, ppc, cppc, udp_check):
    """

    :param uuid: 16bytes, 报文唯一标识
    :param peer_id: 16bytes, sdk的peer_id
    :param file_id: 16bytes, 文件标识
    :param file_url: 256bytes
    :param piece_size: 2bytes, 文件piece大小
    :param ppc: 2bytes
    :param cppc: 2bytes
    :param live_push_server: 64bytes, 预留
    :param udp_check: 是否包含checksum
    :return:
    """
    distinguish = '91'
    token = str(uuid).rjust(32, '0')
    reserved = '0' * 64
    rrpc_id = '0001'
    peer_id = str(peer_id.lower()).rjust(32, '0')
    file_id = str(file_id.lower()).rjust(32, '0')
    file_url = str(binascii.b2a_hex(file_url)).rjust(512, '0')
    piece_size = str(hex(piece_size)[2:-1]).rjust(4, '0')
    ppc = str(hex(ppc)[2:-1]).rjust(4, '0')
    cppc = str(hex(cppc)[2:-1]).rjust(4, '0')
    live_push_server = '0' * 128
    data_combine = distinguish + token + reserved + rrpc_id + peer_id + file_id + file_url + piece_size + ppc + cppc + live_push_server
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def rrpc_leave_leifeng_data(uuid, peer_id, file_id, udp_check):
    """

    :param uuid: 16bytes, 报文唯一标识
    :param peer_id: 16bytes, sdk的peer_id
    :param file_id: 16bytes, 文件标识
    :param udp_check: 是否包含checksum
    :return:
    """
    distinguish = '91'
    token = str(uuid).rjust(32, '0')
    reserved = '0' * 64
    rrpc_id = '0002'
    peer_id = str(peer_id.lower()).rjust(32, '0')
    file_id = str(file_id.lower()).rjust(32, '0')
    # checksum
    data_combine = distinguish + token + reserved + rrpc_id + peer_id + file_id
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def rrpc_p2p_setting(uuid, peer_id, setting, udp_check):
    """

    :param uuid: 16bytes, 报文唯一标识
    :param peer_id: 16bytes, sdk的peer_id
    :param setting: 是否开启节点p2p功能, 为'01'则启用，为'00'则禁用
    :param udp_check: 是否包含checksum
    :return:
    """
    distinguish = '91'
    token = str(uuid).rjust(32, '0')
    reserved = '0' * 64
    rrpc_id = '0003'
    peer_id = str(peer_id.lower()).rjust(32, '0')
    # checksum
    data_combine = distinguish + token + reserved + rrpc_id + peer_id + setting
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def rrpc_rsm_report_data(uuid, peer_id, udp_check):
    """
    2016.09.30 暂未使用
    :param uuid: 16bytes, 报文唯一标识
    :param peer_id: 16bytes, sdk的peer_id
    :param udp_check: 是否包含checksum
    :return:
    """
    distinguish = '91'
    token = str(uuid).rjust(32, '0')
    reserved = '0' * 64
    rrpc_id = '0003'
    peer_id = str(peer_id.lower()).rjust(32, '0')
    data_combine = distinguish + token + reserved + rrpc_id + peer_id
    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def udp_checksum(udp_data):
    """
    根据udp数据生成checksum
    :param udp_data: "810101"
    :return:
    """
    data_binascii = binascii.a2b_hex(udp_data)
    data = bytearray(data_binascii)
    length = len(data)

    t = length >> 3
    rest = length & 7
    # print t, rest
    sum = socket.htons(0x7973)
    for i in range(0, t):
        p = struct.unpack_from("Q", data, i * 8)[0]
        sum = sum ^ p

    if rest:
        temp = bytearray(8)
        for i in range(0, rest):
            temp[i] = data[t * 8 + i]
        last = struct.unpack_from("Q", temp, 0)[0]
        sum = sum ^ last

    sum = ((sum >> 32) ^ sum) & 0xffffffff
    cs = (((sum >> 16) ^ sum) & 0xffff)
    checksum = socket.ntohs(cs)
    checksum_hex = str(hex(checksum)).replace("0x", "")
    return checksum_hex


@print_trace
def pene_query_peer_req(peer_id, udp_check):
    """
    sdk => stun 穿透协议
    :param peer_id:
    :param udp_check
    :return:
    """
    peer_id = str(peer_id.lower()).rjust(32, '0')
    data_combine = "a101{0}".format(peer_id).ljust(36, '0')

    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def pene_penetrate_req(dst_peer_id, src_public_ip, src_public_port, udp_check):

    dst_peer_id = str(dst_peer_id.lower()).rjust(32, '0')
    src_public_ip_split = src_public_ip.split(".")
    src_public_ip = ""
    for i in src_public_ip_split:
        i_hex = str(hex(int(i))[2:]).rjust(2, '0')
        src_public_ip += i_hex
    src_public_port = str(hex(int(src_public_port)))[2:]
    data_combine = "a103{0}01{1}{2}".format(dst_peer_id, src_public_ip, src_public_port).ljust(50, '0')

    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data


@print_trace
def pene_reversing_req(dst_peer_id, src_peer_id, src_public_ip, src_public_port, src_stun_ip, src_stun_port, udp_check):

    dst_peer_id = str(dst_peer_id.lower()).rjust(32, '0')
    src_peer_id = str(src_peer_id.lower()).rjust(32, '0')
    src_public_ip_split = src_public_ip.split(".")
    src_public_ip = ""
    for i in src_public_ip_split:
        i_hex = str(hex(int(i))[2:]).rjust(2, '0')
        src_public_ip += i_hex
    src_public_port = str(hex(int(src_public_port)))[2:]
    src_stun_ip_split = src_stun_ip.split(".")
    src_stun_ip = ""
    for i in src_stun_ip_split:
        i_hex = str(hex(int(i))[2:]).rjust(2, '0')
        src_stun_ip += i_hex
    src_stun_port = str(hex(int(src_stun_port)))[2:]
    data_combine = "a106{0}{1}{2}{3}{4}{5}".format(dst_peer_id, src_peer_id, src_public_ip, src_public_port,
                                                   src_stun_ip, src_stun_port).ljust(92, '0')

    if udp_check:
        checksum = udp_checksum(data_combine)
        send_data = data_combine + checksum
    else:
        send_data = data_combine
    return send_data

if __name__ == '__main__':
    test_data = "810101"
    c = udp_checksum(test_data)
    print c
    a = query_type_req_data(1)
    print a
