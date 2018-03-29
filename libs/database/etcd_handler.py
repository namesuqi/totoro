# coding=utf-8
# Bussiness related Etcd Operation
# Author=JKZ
import json
import etcd
import requests
from libs.const.database import ETCD_CLUSTER_HOST, ETCD_CLUSTER_PORT

ETCD_HOST_1 = ETCD_CLUSTER_HOST[0]
ETCD_PORT = ETCD_CLUSTER_PORT[0]


def read_etcd_key(key_name, key_path=""):
    """
    读取指定目录下指定key中的内容
    :param key_name:
    :param key_path:
    :return:
    """
    client = etcd.Client(host=ETCD_HOST_1, port=ETCD_PORT, allow_redirect=False)
    value_list = {}
    try:
        r = client.read(str(key_path) + str(key_name), recursive=True, sorted=True)
        for child in r.children:
            # print("%s: %s" % (child.key, child.value))
            try:
                dict_value = json.loads(child.value)
            except:
                dict_value = child.value
            value_list[child.key] = dict_value
        return value_list
    except Exception as error:
        # do something
        print error
        return None


def set_etcd_key(key_name, key_value, key_path=""):
    """
    在指定目录下添加指定key-value
    :param key_name: 要添加的key
    :param key_value: value
    :param key_path: 目录，即在该目录下添加该key
    :return:
    """
    client = etcd.Client(host=ETCD_HOST_1, port=ETCD_PORT, allow_redirect=False)
    set_key = str(key_path) + str(key_name)
    if str(key_value).startswith("{") or str(key_value).startswith("["):
        set_value = json.dumps(key_value)
    else:
        set_value = key_value
    client.write(set_key, set_value)
    # print "Set key:", set_key
    # print "Set value:", set_value


def del_etcd_key(key_name, key_path=""):
    """
    删除指定key，若key_name为目录则删除目录和所有子键
    :param key_name: key
    :param key_path:
    :return:
    """
    client = etcd.Client(host=ETCD_HOST_1, port=ETCD_PORT, allow_redirect=False)
    del_key = str(key_path) + str(key_name)
    # print "Delete :", del_key
    try:
        client.delete(del_key, recursive=True)
    except Exception as err:
        return err


def etcd_set_group(group, key_path="", default_value=None, deep_dark=False):
    """
    set一组key-value
    :param group:
    :param key_path:
    :param default_value:
    :param deep_dark:
    :return:
    """
    if default_value is None:
        for k, v in group.iteritems():
            set_etcd_key(k, v, key_path)
    else:
        for k, v in group.iteritems():
            if type(v) == dict and deep_dark:
                for k2, v2 in v.iteritems():
                    v[k2] = default_value
            set_etcd_key(k, v, key_path)


def etcd_del_group(group, key_path=""):
    for k in group.keys():
        del_etcd_key(k, key_path)


if __name__ == "__main__":
    CONFIG_VOD_ONLINE_TEST = {
        "/business/httpdns/v2/domain_group/crazycdn.com": [
            "ts.crazycdn.com",
            "seeds.crazycdn.com",
            "report.crazycdn.com",
            "errlogs.crazycdn.com",
            "stats.crazycdn.com",
            "live-ch.crazycdn.com",
            "upgradev2.crazycdn.com",
            "channel.crazycdn.com",
            "stun2.crazycdn.com",
            "opt.crazycdn.com",
            "control.crazycdn.com",
            "hls.crazycdn.com"
        ],
        "/business/httpdns/v2/domain_ip_map/default": {
            "ts.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
            "seeds.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
            "report.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
            "live-ch.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
            "channel.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
            "stun2.crazycdn.com": {"ips": {"default": ["118.190.148.163"]}, "ttl": 1800},
            "stats.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
            "errlogs.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
            "upgradev2.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
            "opt.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
            "control.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
            "hls.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800}
        },
        "/business/httpdns/v2/areas/default": {
            "ip_group": "default"
        }
    }
    # del_etcd_key("/business/httpdns/v2")
    # etcd_set_group(CONFIG_VOD_ONLINE_TEST)
    read_etcd_key("/business/")


    # res_1 = requests.get("http://172.30.0.23:9500/httpdns/host?host=stun2.crazycdn.com")
    # res_2 = requests.get("http://172.30.0.23:9500/httpdns/hosts?groupName=crazycdn.com")
    # print res_1.status_code, res_1.content
    # print res_2.status_code, res_2.content

