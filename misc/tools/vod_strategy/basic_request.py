# coding=utf-8
# sdk requests, create peer id
import json
import random
import requests
from misc.tools.vod_strategy.const import TS_IP, TS_PORT, HEADERS


def send_login_req(peer_id, version, nat_type, public_ip, public_port, private_ip, private_port, stun_ip, macs):

    login_body = {
           "version": version,
           "natType": nat_type,
           "publicIP": public_ip,
           "publicPort": public_port,
           "privateIP": private_ip,
           "privatePort": private_port,
           "stunIP": stun_ip,
           "macs": macs
    }
    response = requests.post("http://{0}:{1}/session/peers/{2}".format(TS_IP, TS_PORT, peer_id),
                             data=json.dumps(login_body), headers=HEADERS)
    if response.status_code != 200 or "error" in response.content:
        print "login", peer_id, response.status_code, response.content
    return response


def send_hb_req(peer_id):

    response = requests.get("http://{0}:{1}/session/peers/{2}".format(TS_IP, TS_PORT, peer_id), headers=HEADERS)
    if response.status_code != 200 or "error" in response.content:
        print "heartbeat", peer_id, response.status_code, response.content
    return response


def send_lsm_report(peer_id, file_id="", file_status="", universe=True, withfile=True):
    """

    :param peer_id:
    :param file_id:
    :param file_status:
    :param universe:
    :param withfile: 是否汇报缓存文件
    :return:
    """

    lsm_body = {
       "diskTotal": 1073741824,  # 1G
       "diskFree": 1073741824,
       "lsmTotal": 1073741824,
       "lsmFree": 1073741824,
       "universe": universe,
       "files": [
           {
                "file_id": file_id,
                "ppc": 304,
                "psize": 1392,
                "cppc": 1,
                "stat": file_status
            }
        ]
    }
    if withfile is not True:
        lsm_body["files"] = []
    response = requests.post("http://{0}:{1}/distribute/peers/{2}".format(TS_IP, TS_PORT, peer_id),
                             data=json.dumps(lsm_body), headers=HEADERS)
    if response.status_code != 200 or "error" in response.content:
        print "lsm report", peer_id, response.status_code, response.content
    return response


def create_peer_id(peer_num):
    peer_id_list = []
    for n in range(peer_num):
        peer_id = "66666666"
        for i in range(24):
            peer_id += '0123456789ABCDEF'[random.randint(0, 15)]
        peer_id_list.append(peer_id)

    return peer_id_list


