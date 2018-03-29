# coding=utf-8
"""
操作MongoDB数据库的底层库

__author__ = 'zsw'

"""

import pymongo
import time


def get_info_by_peer_id(mongodb_host, mongodb_port, peer_ids):
    """
    根据peer_id查询cdn_peer表
    :param mongodb_host:
    :param mongodb_port:
    :param peer_ids:
    :return:
    """
    client = pymongo.MongoClient(mongodb_host, mongodb_port)
    db = client.cdn_peer
    cdn_peer = db.cdn_peer
    info_list = []  # for return
    for peer_id in peer_ids:
        peer_items = cdn_peer.find({"peer_id": peer_id})
        for peer_info in peer_items:
            print peer_info
            info_list.append(peer_info)
    return info_list


def get_info_by_ip(mongodb_host, mongodb_port, pub_ip):
    """
    根据ip信息查询cdn_peer表
    :param mongodb_host:
    :param mongodb_port:
    :param pub_ip:
    :return:
    """
    client = pymongo.MongoClient(mongodb_host, mongodb_port)
    db = client.cdn_peer
    cdn_peer = db.cdn_peer
    peer_items = cdn_peer.find({"ip": pub_ip})
    print "-----------get info by ip from mongo-----------"
    info_list = []
    for peer_info in peer_items:
        print peer_info
        info_list.append(peer_info)
    return info_list


def add_info_cdn_peer(mongodb_host, mongodb_port, peer_ids, ip="123.123.123.123", lsmSize=0, version="3.1.0", macs="",
                      deviceInfo="{}"):
    """
    在cdn_peer表中插入节点信息
    :param mongodb_host:
    :param mongodb_port:
    :param peer_ids:
    :param ip:
    :param lsmSize:
    :param version:
    :param macs:
    :param deviceInfo:
    :return:
    """
    now_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    client = pymongo.MongoClient(mongodb_host, mongodb_port)
    db = client.cdn_peer
    cdn_peer = db.cdn_peer
    print "-----------add info to mongo-----------"
    for peer_id in peer_ids:
        cdn_peer.save({"peer_id": peer_id, "lsmSize": lsmSize, "version": version, "ip": ip, "macs": macs,
                       "deviceInfo": deviceInfo, "modifiedTime": now_time})
        # peer_items = cdn_peer.find({"peer_id": peer_id})
        # for peer_info in peer_items:
        #     print peer_info


def del_info_cdn_peer(mongodb_host, mongodb_port, peer_ids):
    """
    慎用，db.remove()将删除所有记录
    :param mongodb_host:
    :param mongodb_port:
    :param peer_ids:
    :return:
    """
    client = pymongo.MongoClient(mongodb_host, mongodb_port)
    db = client.cdn_peer
    cdn_peer = db.cdn_peer
    for peer_id in peer_ids:
        cdn_peer.remove({"peer_id": peer_id})


def get_seed_info_by_peer_id(mongodb_host, mongodb_port, peer_ids):
    """
    根据peer_id查询cdn_file_seed_map表
    :param mongodb_host:
    :param mongodb_port:
    :param peer_ids:
    :return:
    """
    client = pymongo.MongoClient(mongodb_host, mongodb_port)
    conn = client.cdn_file_seed_map
    db = conn.cdn_file_seed_map
    info_list = []  # for return
    for peer_id in peer_ids:
        peer_items = db.find({"peer_id": peer_id})
        for peer_info in peer_items:
            print peer_info
            info_list.append(peer_info)
    return info_list


def get_info_by_para(mongodb_host, mongodb_port, table_name, collection_name, **args):
    """
    根据指定条件查询对应信息
    :param mongodb_host:
    :param mongodb_port:
    :param table_name:
    :param collection_name:
    :param args: 查询条件
    :return:
    """
    client = pymongo.MongoClient(mongodb_host, mongodb_port)
    db = client[table_name]
    print table_name, "collections:", db.collection_names()
    db_collection = db[collection_name]
    info_list = []  # for return
    i = 0
    print "search condition:", args
    if len(args) == 0:
        info_items = db_collection.find()
        for piece_info in info_items:
            print i, piece_info
            info_list.append(piece_info)
            i += 1
    else:
        info_items = db_collection.find(args)
        for piece_info in info_items:
            print i, piece_info
            info_list.append(piece_info)
            i += 1
    return info_list


def del_info_by_para(mongodb_host, mongodb_port, table_name, collection_name, **args):
    """
    根据指定条件删除对应信息
    :param mongodb_host:
    :param mongodb_port:
    :param table_name:
    :param collection_name:
    :param args:
    :return:
    """
    client = pymongo.MongoClient(mongodb_host, mongodb_port)
    db = client[table_name]
    db_collection = db[collection_name]
    info_list = []  # for return
    if len(args) == 0:
        print "！！！ Please input the args will be removed"
    else:
        info_items = db_collection.remove(args)
        # for piece_info in info_items:
        #     print piece_info
        #     info_list.append(piece_info)
    return info_list


if __name__ == "__main__":
    get_info_by_para("192.168.1.194", 27017, "test", "server_node", name="dir", version="safdasfsadfsafassd")
    # get_info_by_para("192.168.1.194", 27017, "test", "server_node")
