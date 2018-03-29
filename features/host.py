# coding=utf-8
# variables to support different test environment
# for example: local, online, product and so on
# please set your AUTO_ENV before run test (e.g. export AUTO_ENV=local_test)
# __author__ = 'liwenxuan'

import os
import socket

# -------------------------------------------------------------------------------------------------------------

# support local_test and online_test
run_env = os.environ.get("AUTO_ENV", None)
# run_env = "local_test"
# run_env = "online_test"

# -------------------------------------------------------------------------------------------------------------

# defaults
domains = {
    "JENKINS": socket.gethostbyname(socket.gethostname()),  # 通过socket解析出的本机ip, 目前支持还不太好

    "CHANNEL_HOST": "channel.crazycdn.com",
    "CHANNEL_PORT": 80,  # 9665

    "PUSH_HUB_HOST": "push-hub.crazycdn.com",
    "PUSH_HUB_PORT": 8001,

    "STUN_HUB_HOST": "stun-hub.ys-internal.com",  # "stun-hub.crazycdn.com"
    "STUN_HUB_PORT": 8000,

    "STUN2_HOST": "stun2.crazycdn.com",
    # "STUN_PORT": 0,

    "TS_HOST": "ts.crazycdn.com",
    "TS_PORT": 80,  # 9510

    "SEEDS_HOST": "seeds.crazycdn.com",
    "SEEDS_PORT": 80,

    "REPORT_HOST": "report.crazycdn.com",
    "REPORT_PORT": 80,

    "VOD_PUSH_HOST": "push.crazycdn.com",
    "VOD_PUSH_PORT": 9529,

    "REDIS_SINGLE_HOST": "redis-stun.ys-internal.com",
    "REDIS_SINGLE_PORT": 6379,

    "REDIS_CLUSTER_HOST": ["redis-groupA-11.ys-internal.com",
                           "redis-groupA-21.ys-internal.com",
                           "redis-groupA-31.ys-internal.com"],
    "REDIS_CLUSTER_PORT": [6380, 6381, 6382],  # local
    # "REDIS_CLUSTER_PORT": [6379, 6379, 6379],  # online

    "ETCD_CLUSTER_HOST": ["etcd1.ys-internal.com",
                          "etcd2.ys-internal.com",
                          "etcd3.ys-internal.com"],
    "ETCD_CLUSTER_PORT": [2379, 2379, 2379],

    "HTTPDNS_HOST": "httpdns.crazycdn.com",
    "HTTPDNS_PORT": 9500,

    "DIR_HOST": "dir.crazycdn.com",
    "DIR_PORT": 9521,

    "UPGRADE_CONTROLLER_HOST": "updatecontrol.crazycdn.com",
    "UPGRADE_CONTROLLER_PORT": 9550,

    "UPGRADE_HOST": "upgradev2.crazycdn.com",
    "UPGRADE_PORT": 9540,
}

# -------------------------------------------------------------------------------------------------------------

# local test environment related variable and consts
local_test = {
    "JENKINS": "192.168.1.102",

    "CHANNEL_HOST": "192.168.1.102",
    "CHANNEL_PORT": 9665,

    "PUSH_HUB_HOST": "192.168.1.100",
    "PUSH_HUB_PORT": 8001,

    "STUN_HUB_HOST": "192.168.1.101",
    "STUN_HUB_PORT": 8000,

    "STUN2_HOST": "192.168.1.102",
    # "STUN_PORT": 0,

    "TS_HOST": "192.168.1.100",
    "TS_PORT": 9510,

    "VOD_PUSH_HOST": "192.168.1.102",
    "VOD_PUSH_PORT": 9529,

    "REDIS_SINGLE_HOST": "192.168.1.102",
    "REDIS_SINGLE_PORT": 6379,

    "REDIS_CLUSTER_HOST": ["192.168.1.102", "192.168.1.102", "192.168.1.102"],
    "REDIS_CLUSTER_PORT": [6380, 6381, 6382],

    "ETCD_CLUSTER_HOST": ["192.168.1.251", "192.168.1.252", "192.168.1.253"],
    "ETCD_CLUSTER_PORT": [2379, 2379, 2379],

    "HTTPDNS_HOST": "",  # not ready for local
    "HTTPDNS_PORT": 9500,

    "DIR_HOST": "192.168.1.241",
    "DIR_PORT": 9521,

    "UPGRADE_CONTROLLER_HOST": "192.168.1.195",
    "UPGRADE_CONTROLLER_PORT": 9550,

    "UPGRADE_HOST": "192.168.1.195",
    "UPGRADE_PORT": 9540,
}

# -------------------------------------------------------------------------------------------------------------

# online test environment related variable and consts
online_test = {
    "JENKINS": "172.30.0.29",

    "CHANNEL_HOST": "172.30.0.24",  # "118.190.150.143"
    "CHANNEL_PORT": 9665,

    "PUSH_HUB_HOST": "172.30.0.35",
    "PUSH_HUB_PORT": 8001,

    "STUN_HUB_HOST": "172.30.0.25",
    "STUN_HUB_PORT": 8000,

    "STUN2_HOST": "172.30.0.17",  # "118.190.148.163"
    # "STUN_PORT": 0,

    "TS_HOST": "172.30.0.18",  # "118.190.150.143"
    "TS_PORT": 9510,

    "VOD_PUSH_HOST": "172.30.0.32",  # "118.190.150.143"
    "VOD_PUSH_PORT": 9529,

    "REDIS_SINGLE_HOST": "172.30.0.19",
    "REDIS_SINGLE_PORT": 6379,

    "REDIS_CLUSTER_HOST": ["172.30.0.20", "172.30.0.21", "172.30.0.22"],
    "REDIS_CLUSTER_PORT": [6379, 6379, 6379],

    "ETCD_CLUSTER_HOST": ["172.30.0.26", "172.30.0.27", "172.30.0.28"],
    "ETCD_CLUSTER_PORT": [2379, 2379, 2379],

    "HTTPDNS_HOST": "172.30.0.23",  # "118.178.213.127"
    "HTTPDNS_PORT": 9500,

    "DIR_HOST": "172.30.0.31",
    "DIR_PORT": 9521,

    "UPGRADE_CONTROLLER_HOST": "",  # 线上暂未部署
    "UPGRADE_CONTROLLER_PORT": 9550,

    "UPGRADE_HOST": "",  # 线上暂未部署
    "UPGRADE_PORT": 9540,
}

# -------------------------------------------------------------------------------------------------------------

# support local_test and online_test
global_env = {
    "local_test": local_test,
    "online_test": online_test,
}

# -------------------------------------------------------------------------------------------------------------



