# coding=utf-8
"""
Business keyword to control redis cluster
reconstructed by Zeng YueTian
2017-9-6
"""

import json
from simplejson import JSONEncoder
from rediscluster import StrictRedisCluster
from libs.const.database import REDIS_CLUSTER_HOST, REDIS_CLUSTER_PORT

startup_nodes = [{"host": host, "port": port} for host, port in zip(REDIS_CLUSTER_HOST, REDIS_CLUSTER_PORT)]
rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)


def redis_cluster_string_get(key):
    """
    已经重构
    返回该key(string类型)对应的value,ttl
    redis command prototype: get key
    :param key:
    :return: dict格式{"ttl": ttl, "value": value}
    """
    result = dict()
    if rc.exists(key):
        v = json.loads(rc.get(key))
        result["value"] = v
        result["ttl"] = rc.ttl(key)

    return result


def redis_cluster_delete_key(key):
    """
    已经重构
    删除指定key
    :param key:
    :return:
    """
    rc.delete(key)
    # print '{0}is delete'.format(key)


def redis_cluster_setex_pnic(ttl, peer_id, sdk_version, nat_type, public_ip, public_port, private_ip, private_port,
                             province_id, isp_id, city_id, stun_ip, country="CN"):
    """
    已经重构
    在redis中写入某节点的PNIC信息，并设定其有效存活时间
    """
    key = "PNIC_" + str(peer_id)

    value = {
        "peer_id": str(peer_id),
        "version": str(sdk_version),
        "natType": int(nat_type),
        "publicIP": str(public_ip),
        "publicPort": int(public_port),
        "privateIP": str(private_ip),
        "privatePort": int(private_port),
        "country": str(country),
        "province_id": str(province_id),
        "isp_id": str(isp_id),
        "city_id": str(city_id),
        "stunIP": str(stun_ip)
    }
    # 将dict转成json格式
    value = JSONEncoder().encode(value)
    rc.setex(key, int(ttl), value)


def redis_cluster_fosc_add(fid, isp, peer_id, version, nat_type, public_ip, public_port, private_ip,
                           private_port, stun_ip, cppc=1, ppc=304):
    """
    在FOSC中set value，若非必要，尽量使用cache_report或control_report请求汇报，由ts-go服务器写入FOSC
    目前服务器维护seed list不只单单使用FOSC，还涉及到LFC，LFCacheManageZset
    """
    key = "{FOSC_" + str(fid) + "_" + str(isp) + "}"
    value = {
        "peer_id": str(peer_id),
        "version": str(version),
        "natType": int(nat_type),
        "publicIP": str(public_ip),
        "publicPort": int(public_port),
        "privateIP": str(private_ip),
        "privatePort": int(private_port),
        "stunIP": str(stun_ip),
        "cppc": int(cppc),
        "ppc": int(ppc)
    }
    # 将dict转成json格式
    value = JSONEncoder().encode(value)
    rc.sadd(key, value)


def redis_cluster_card_key(card_key, *args):
    """
    统计该key对应集合中的元素数量
    :param card_key:
    :param args: 拼接key
    :return:
    """
    if args:
        for i in args:
            card_key = str(card_key) + str(i)

    # 判断该key对应的类型
    key_type = rc.type(card_key)
    if str(key_type) == "set":
        element_nums = rc.scard(card_key)
    elif str(key_type) == "zset":
        element_nums = rc.zcard(card_key)
    else:
        # print "Type should be set or zset !!!"
        element_nums = 0
    return element_nums


def redis_cluster_set_get(smembers_key, *args):
    """
    返回该key对应集合的所有元素
    redis command prototype: SMEMBERS key
    :param smembers_key:
    :param args: 拼接key，传参举例：cluster_set_get("{FOSC_", file_id, "_", isp, "}")
    :return:
    """
    if args:
        for i in args:
            smembers_key = str(smembers_key) + str(i)
    val = rc.smembers(smembers_key)

    members_list = []
    for i in val:
        members_list.append(json.loads(i))

    return members_list


def redis_cluster_string_match(match_key):
    """
    匹配相关key
    :param match_key: eg. "PNIC*"
    :return:
    """
    match_keys = rc.keys(str(match_key))
    match_result = dict()
    for i in match_keys:
        print i
        match_result[i] = json.loads(rc.get(i))
    return match_result


def byteify(input_json):
    """
    handle json unicode to str
    :param input_json:
    :return:
    """
    if isinstance(input_json, dict):
        return {byteify(key): byteify(value) for key, value in input_json.iteritems()}
    elif isinstance(input_json, list):
        return [byteify(element) for element in input_json]
    elif isinstance(input_json, unicode):
        return input_json.encode('utf-8')
    else:
        return input


def redis_cluster_delete_keys(prefix, *args):
    """
    delete all key with specified prefix
    :param prefix:
    :return:
    """
    # 如果有多个参数，将多个参数拼接成一个key
    if args:
        for i in args:
            prefix = str(prefix) + str(i)
    keys = rc.keys("*" + prefix + "*")
    for key in keys:
        rc.delete(key)


def redis_cluster_sadd_pdfc(peer_id, file_id, psize, ppc, operation, src=0):
    """
    定向推送删除任务到某个peer
    :param peer_id:
    :param file_id:
    :param psize:
    :param ppc:
    :param operation:
    :param src:
    :return:
    """
    key = "PDFC_" + str(peer_id)
    value = {
        "file_id": str(file_id),
        "psize": int(psize),
        "ppc": int(ppc),
        "operation": str(operation),
        "src": src
    }
    # 将dict转成json格式
    value = JSONEncoder().encode(value)
    rc.sadd(key, value)


def redis_cluster_sadd_ppfc(peer_id, file_id, fsize, psize, ppc, operation, src=0, server_host=None, server_port=None):
    """
    定向推送任务到指定peer id
    :param peer_id:
    :param file_id:
    :param fsize:
    :param psize:
    :param ppc:
    :param operation:
    :param src:
    :param server_host: eg. "push.crazycdn.com","127.0.0.1"
    :param server_port: eg. 80, 9529
    :return:
    """
    key = "PDFC_" + str(peer_id)
    value = {
        "file_id": str(file_id),
        "fsize": int(fsize),
        "psize": int(psize),
        "ppc": int(ppc),
        "operation": str(operation),
        "src": src
    }
    if server_host is not None and server_port is not None:
        value["server"] = str(server_host)
        value["port"] = int(server_port)
    # 将dict转成json格式
    value = JSONEncoder().encode(value)
    rc.sadd(key, value)


if __name__ == "__main__":
    # cluster_set_add("00010026408B9F4AB0E85524E25043D3", "272E603BA82C4B0E817A124960E1D1AD", 1, '3.0.0', 1,
    #                 '1.1.1.1', 56379, '1.2.3.4', 11331)
    # cluster_get_pnic("0000000447904EE184946F885D0BFDCA")

    # FOSC_KEY = "{FOSC_85FA513E3D6E0A180657D2EA0C1E9DC1_000000}"
    # cluster_card_key("LFCacheManageZset")

    # file_id = file_id = "".ljust(32, "F")
    # cluster_delete_keys("{FOSC_", file_id)
    # ISP_LIST = ["100017", "100026", "000000"]
    # for isp in ISP_LIST:
    #     print "--------------%s------------------" % isp
    #     cluster_set_get("{FOSC_", file_id, "_", isp, "}")

    s = redis_cluster_string_get("PNIC_0000000012345123451234512345ABCD")
    print s
