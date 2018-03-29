# coding=utf-8
"""
Bussiness related Redis Operation
Author: JKZ
"""
import json
import redis
from string import Template
from simplejson import JSONEncoder
from libs.const.database import *

rc = redis.StrictRedis(host=REDIS_SINGLE_HOST, port=REDIS_SINGLE_PORT, db=0)

# -------------------------------------------------------------------------------------------------------------


def redis_single_delete_keys(prefix, *args):
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


def redis_single_add_stun_peer(peer_id, pub_ip, pub_port, pri_ip, pri_port, nat_type):
    """
    add key STUN_${peer_id} to redis-single
    :param peer_id: str(one peer) or list(peers)
    :param pub_ip:
    :param pri_ip:
    :param pub_port:
    :param pri_port:
    :param nat_type:
    :return:
    """
    if type(peer_id) != list:
        peer_id = [peer_id]

    for pid in peer_id:
        key = Template('STUN_$peerid')
        KEY = key.substitute(peerid=pid)
        value = Template(
         "{\"nat_type\":$nat_type,\"pub_ip\":\"$pub_ip\",\"pub_port\":$pub_port,\"pri_ip\":\"$pri_ip\","
         "\"pri_port\":$pri_port}"
        )
        VALUE = value.substitute(nat_type=nat_type, pub_ip=pub_ip, pub_port=pub_port, pri_ip=pri_ip, pri_port=pri_port)
        rc.setex(KEY, 300, VALUE)


def redis_single_get_stun_peer(peer_id):
    """
    根据peer_id查询redis中STUN_[peer_id]的信息
    :param peer_id:
    :return:
    """
    keys_info = ["nat_type", "pub_port", "pri_port", "pri_ip", "pub_ip"]
    key = Template('STUN_$peerid')
    KEY = key.substitute(peerid=peer_id)
    stun_peer_value = rc.get(KEY)

    stun_peer_info = []
    if stun_peer_value:
        stun_peer_json = json.loads(stun_peer_value)  # str -> json
        # print a.keys()
        # print a.values()
        for key in keys_info:
            stun_peer_info.append(stun_peer_json[key])
        return stun_peer_info
    else:
        return None


def redis_single_zadd_pgpfc(user_id, task_count, file_id, fsize, psize, ppc, operation, src, priority,
                            server_host=None, server_port=None):
    """
    推送到某个user id的task列表
    :param user_id:
    :param task_count: 任务份数
    :param file_id:
    :param fsize:
    :param psize:
    :param ppc:
    :param operation:
    :param src:
    :param priority:
    :param server_host:
    :param server_port:
    :return:
    """
    key = "PGPFC_" + str(user_id)
    if operation == "download":
        value = {
            "file_id": str(file_id),
            "fsize": int(fsize),
            "psize": int(psize),
            "ppc": int(ppc),
            "operation": str(operation),
            "src": src,
            "priority": int(priority)
        }
        if server_host is not None and server_port is not None:
            value["server"] = str(server_host)
            value["port"] = int(server_port)
    elif operation == "delete":
        value = {
            "file_id": str(file_id),
            "psize": int(psize),
            "ppc": int(ppc),
            "operation": str(operation),
            "src": src,
            "priority": int(priority)
        }
    else:
        raise
    # 将dict转成json格式
    value = JSONEncoder().encode(value)
    rc.zadd(key, task_count, value)

# -------------------------------------------------------------------------------------------------------------


def redis_single_get_list(key_name, start=0, end=-1):
    """
    获取列表元素
    :param key_name: 列表类型的key
    :param start: 获取列表范围的起始下标
    :param end: 获取列表范围的结束下标
    :return: []
    """
    return rc.lrange(key_name, int(start), int(end))


def redis_single_get_zset(key_name, start=0, end=-1, with_scores=False, desc=False):
    """
    获取有序集合的元素
    :param key_name: 有序集合类型的key
    :param start: 获取范围的起始下标
    :param end: 获取范围的结束下标
    :param with_scores: 是否需要获取分数
    :param desc: 是否需要按分数降序排列
    :return: [value, value, ...] or [(value, score), (), ...]
    """
    return rc.zrange(key_name, int(start), int(end), withscores=bool(with_scores), desc=bool(desc))


def redis_single_delete_key(key_name):
    # 删除特定的某个key
    rc.delete(key_name)


def redis_single_add_zset(key_name, score, value):
    """
    在有序集合中, 添加元素及其分数
    :param key_name: 有序集合类型的key
    :param score: 元素的分数
    :param value: 元素的值
    :return:
    """
    rc.zadd(key_name, float(score), json.dumps(value))


def redis_single_add_list(key_name, value):
    """
    添加列表元素
    :param key_name: 列表类型的key
    :param value: 元素的值
    :return:
    """
    rc.lpush(key_name, json.dumps(value))


def redis_single_check_exists(key_name):
    # 检查指定key是否存在
    return rc.exists(key_name)

# -------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # redis_single_zadd_pgpfc(user_id="66666666", task_count=10, file_id="7FF5B13044EB44FBA4FAAA85F9400643",
    #                         fsize=775134238, psize=1392, ppc=304, operation="download", src=0, priority=10)
    pass

