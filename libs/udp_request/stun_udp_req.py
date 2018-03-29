# coding=utf-8
"""
stun related api test keyword for udp, YSSTUN, YSRRPC

__author__ = 'zsw'

"""

from libs.udp_request.stun_udp_data import *
from libs.const.stun_udp import *
from libs.udp_request.udp_request import *
from libs.decorator.trace import *


@print_trace
def sdk_query_type_req(stun_udp_host, stun_udp_port, step=1, listening_port=60000, udp_check=False):
    """
    模拟sdk向stun-srv发送query_type_req
    :param stun_udp_host: udp包的接收方地址
    :param stun_udp_port: udp包的接收方端口
    :param step: STUNV1协议的step，目的端口为9000, 则为1, 目的端口为9002, 则为2
    :param listening_port:本地发送udp包的监听端口
    :param udp_check: 是否包含checksum
    :return:
    """
    send_data = query_type_req_data(step, udp_check)

    response = send_udp_request(
        '[SdkQueryTypeReq]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def stun_query_type_rsp(stun_udp_host, stun_udp_port, pub_ip, pub_port, step=1, listening_port=60000, udp_check=False):
    """
    向stun-srv发送query_type_rsp
    :param stun_udp_host:
    :param stun_udp_port:
    :param pub_ip: sdk的公网地址
    :param pub_port: sdk的公网port
    :param step: sdk向stun的9000端口发送C_STUN_QUERY_TYPE_REQ时, 可获得stun从9000端口以及9001端口的回复, 来自
    9000端口的回复step为1, 来自9001的回复step为3, sdk向stun的9002端口发送C_STUN_QUERY_TYPE_REQ时，可获得stun
    从9002端口以及9001端口的回复, 来自9002端口的回复step为2, 来自9001的回复step为4
    :param listening_port: 本地发送udp包的监听端口
    :param udp_check: 是否包含checksum
    :return:
    """
    send_data = query_type_rsp_data(pub_ip, pub_port, step, udp_check)

    response = send_udp_request(
        '[SdkQueryTypeRsp]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def sdk_nat_update_req(stun_udp_host, stun_udp_port, peer_id, nat_type, pri_ip, pri_port, listening_port=60000, udp_check=False):
    """
    向stun-srv发送nat_update_req
    :param stun_udp_host:
    :param stun_udp_port:
    :param peer_id: sdk的peer_id
    :param nat_type: sdk自己探测出来的NAT类型
    :param pri_ip: sdk的私网IP
    :param pri_port: sdk的私网port
    :param listening_port:
    :param udp_check: 是否包含checksum
    :return:
    """
    send_data = nat_update_req_data(peer_id, nat_type, pri_ip, pri_port, udp_check)

    response = send_udp_request(
        '[SdkNatUpdateReq]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def stun_nat_update_rsp(stun_udp_host, stun_udp_port, rsp_code=0, listening_port=60000, udp_check=False):
    """
    向stun-srv发送nat_update_rsp
    :param stun_udp_host:
    :param stun_udp_port:
    :param rsp_code: 状态码
    :param listening_port:
    :param udp_check: 是否包含checksum
    :return:
    """
    send_data = nat_update_rsp_data(rsp_code, udp_check)

    response = send_udp_request(
        '[SdkNatUpdateRsp]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def sdk_nat_quit(stun_udp_host, stun_udp_port, peer_id, listening_port=60000, udp_check=False):
    """
    向stun-srv发送nat_quit
    :param stun_udp_host:
    :param stun_udp_port:
    :param peer_id:
    :param listening_port:
    :param udp_check: 是否包含checksum
    :return:
    """
    send_data = nat_quit_data(peer_id, udp_check)

    response = send_udp_request(
        '[SdkNatQuit]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        1
    )
    return response


@print_trace
def sdk_rrpc_ack(stun_udp_host, stun_udp_port, uuid, peer_id, result, listening_port=60000, udp_check=False):
    """
    向stun-srv发送rrpc_ack
    :param uuid: 报文唯一标识
    :param peer_id:
    :param result:
    :param listening_port:
    :param stun_udp_host:
    :param stun_udp_port:
    :param udp_check:
    :return:
    """
    send_data = rrpc_ack_data(uuid, peer_id, result, udp_check)

    response = send_udp_request(
        '[SdkRrpcAck]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def stun_rrpc_join_lf(stun_udp_host, stun_udp_port, uuid, peer_id, file_id, file_url, piece_size, ppc, cppc, listening_port=60000, udp_check=False):
    """
    向stun-srv发送rrpc_join_lf
    :param uuid:
    :param peer_id:
    :param file_id:
    :param file_url:
    :param piece_size:
    :param ppc:
    :param cppc:
    :param listening_port:
    :param stun_udp_host:
    :param stun_udp_port:
    :param udp_check:
    :return:
    """
    send_data = rrpc_join_leifeng_data(uuid, peer_id, file_id, file_url, piece_size, ppc, cppc, udp_check)

    response = send_udp_request(
        '[SdkRrpcJoinLf]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def stun_rrpc_leave_lf(stun_udp_host, stun_udp_port, uuid, peer_id, file_id, listening_port=60000, udp_check=False):
    """
    向stun-srv发送rrpc_leave_lf
    :param uuid:
    :param peer_id:
    :param file_id:
    :param listening_port:
    :param stun_udp_host:
    :param stun_udp_port:
    :param udp_check:
    :return:
    """
    send_data = rrpc_leave_leifeng_data(uuid, peer_id, file_id, udp_check)

    response = send_udp_request(
        '[SdkRrpcLeaveLf]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def stun_rrpc_p2p_setting(stun_udp_host, stun_udp_port, uuid, peer_id, setting, listening_port=60000, udp_check=False):
    """
    向stun-srv发送p2p_setting
    :param uuid:
    :param peer_id:
    :param setting: 是否开启节点p2p功能, 为'01'则启用，为'00'则禁用
    :param listening_port:
    :param stun_udp_host:
    :param stun_udp_port:
    :param udp_check:
    :return:
    """
    send_data = rrpc_p2p_setting(uuid, peer_id, setting, udp_check)

    response = send_udp_request(
        '[SdkRrpcP2pSetting]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def sdk_pene_query_peer_req(stun_udp_host, stun_udp_port, peer_id, listening_port=60000, udp_check=False):
    """
    向stun发送穿透查询协议
    :param stun_udp_host:
    :param stun_udp_port:
    :param peer_id:
    :param listening_port:
    :param udp_check:
    :return:
    """
    send_data = pene_query_peer_req(peer_id, udp_check)

    response = send_udp_request(
        '[PeneQueryPeer]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def sdk_pene_penetrate_req(stun_udp_host, stun_udp_port, dst_peer_id, src_public_ip, src_public_port, 
                           listening_port=60000, udp_check=False):
    print src_public_port
    send_data = pene_penetrate_req(dst_peer_id, src_public_ip, src_public_port, udp_check)

    response = send_udp_request(
        '[SdkPenePenetrateReq]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        1
    )
    return response


@print_trace
def sdk_pene_reserving_req(stun_udp_host, stun_udp_port, dst_peer_id, src_peer_id, src_public_ip, src_public_port, 
                           src_stun_ip, src_stun_port,listening_port=60000, udp_check=False):
    send_data = pene_reversing_req(dst_peer_id, src_peer_id, src_public_ip, src_public_port, src_stun_ip, src_stun_port, udp_check)

    response = send_udp_request(
        '[SdkPeneReservingReq]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        1
    )
    return response


@print_trace
def sdk_query_type_req_indefinite(stun_udp_host, stun_udp_port, step=1, listening_port=60000, udp_check=False):
    """
    模拟sdk向stun-srv发送query_type_req
    :param stun_udp_host: udp包的接收方地址
    :param stun_udp_port: udp包的接收方端口
    :param step: STUNV1协议的step，目的端口为9000, 则为1, 目的端口为9002, 则为2
    :param listening_port:本地发送udp包的监听端口
    :param udp_check:
    :return:
    """
    print stun_udp_host, stun_udp_port, step
    send_data = query_type_req_data_indefinite(step, udp_check)

    response = send_udp_request(
        '[SdkQueryTypeReq]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def sdk_nat_update_req_indefinite(stun_udp_host, stun_udp_port, peer_id, nat_type, pri_ip, pri_port, listening_port=60000, udp_check=False):
    """
    向stun-srv发送nat_update_req
    :param stun_udp_host:
    :param stun_udp_port:
    :param peer_id: sdk的peer_id
    :param nat_type: sdk自己探测出来的NAT类型
    :param pri_ip: sdk的私网IP
    :param pri_port: sdk的私网port
    :param listening_port:
    :param udp_check:
    :return:
    """
    send_data = nat_update_req_data_indefinite(peer_id, nat_type, pri_ip, pri_port, udp_check)

    response = send_udp_request(
        '[SdkNatUpdateReq]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


@print_trace
def sdk_nat_quit_indefinite(stun_udp_host, stun_udp_port, peer_id, listening_port=60000, udp_check=False):
    """
    向stun-srv发送nat_quit
    :param stun_udp_host:
    :param stun_udp_port:
    :param peer_id:
    :param listening_port:
    :param udp_check:
    :return:
    """
    send_data = nat_quit_data_indefinite(peer_id, udp_check)

    response = send_udp_request(
        '[SdkNatQuit]',
        stun_udp_host,
        stun_udp_port,
        send_data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response
