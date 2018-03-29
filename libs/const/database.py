# coding=utf-8
"""
global constant for database
auto test use xxx.auto.cloutropy.com.cn as domain name
__author__ = 'zengyuetian'

"""

from features.host import *

# use domain name for different test environments
# the /etc/hosts will give correct ip address

MYSQL_HOST = "192.168.1.250"
MYSQL_PORT = 3306
MYSQL_USER = "ysboss"
MYSQL_PASSWORD = "Yunshang2014"
MYSQL_DATABASE = "boss"


MYSQL_TBBOX = "tbbox"
MYSQL_BOSS = "boss"
MYSQL_CONTROL = "control"

MONGODB_HOST = "192.168.4.208"

# database
MONGO_CDN_FILE = "cdn_file"
MONGO_CDN_FILE_SEED_MAP = "cdn_file_seed_map"
MONGO_CDN_IP_INFO = "cdn_ip_info"
MONGO_CDN_PEER = "cdn_peer"

MONGODB_PORT = 27017
MONGODB_USER = ""
MONGODB_PASSWORD = ""


REDIS_HOST = "192.168.4.237"
# REDIS_HOST = "10.5.100.2"
REDIS_PORT = 6379
REDIS_USER = ""
REDIS_PASSWORD = ""

# -------------------------------------------------------------------------------------------------------------

REDIS_SINGLE_HOST = global_env.get(run_env, domains)["REDIS_SINGLE_HOST"]
REDIS_SINGLE_PORT = global_env.get(run_env, domains)["REDIS_SINGLE_PORT"]

REDIS_CLUSTER_HOST = global_env.get(run_env, domains)["REDIS_CLUSTER_HOST"]
REDIS_CLUSTER_PORT = global_env.get(run_env, domains)["REDIS_CLUSTER_PORT"]

ETCD_CLUSTER_HOST = global_env.get(run_env, domains)["ETCD_CLUSTER_HOST"]
ETCD_CLUSTER_PORT = global_env.get(run_env, domains)["ETCD_CLUSTER_PORT"]

# -------------------------------------------------------------------------------------------------------------




