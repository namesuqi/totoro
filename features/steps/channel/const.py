# coding=utf-8
# author: JKZ
# channel_server related const

from features.host import *

# -------------------------------------------------------------------------------------------------------------

CHANNEL_HOST = global_env.get(run_env, domains)["CHANNEL_HOST"]  # "channel.crazycdn.com"
CHANNEL_PORT = global_env.get(run_env, domains)["CHANNEL_PORT"]

# -------------------------------------------------------------------------------------------------------------

CPPC = 1

PPC = 256

PSIZE = 1392

# -------------------------------------------------------------------------------------------------------------

USER_DEMO = "demo"
USER_ID_DEMO = "00002222"
DEMO_FILE_URL1 = "http://c23.myccdn.info/a6d33f8c1bc5dbf00e5b1125d4c62ceb/5a87af7a/mp4/Avatar_15Mbps.mp4"
DEMO_FILE_ID1 = "3F6A3649BBE84E5898C410C730666B8C"
PEER_ID = "00002222B2C543E39C24E6AED994BF85"

# -------------------------------------------------------------------------------------------------------------
# master列表相关信息
MASTER_FILE_INFO = {"playlist": "http%3a%2f%2fyunshang.cloutropy.com%2fdemo%2fhls%2fyunshang-master.m3u8",
                    "user": "demo"}
# media列表相关信息
MEDIA_FILE_INFO = {"playlist": "http%3a%2f%2fyunshang.cloutropy.com%2fdemo%2fhls%2focean_4m%2fdemo_ocean_4mbps.m3u8",
                   "user": "demo",
                   "data_file_id": "12A387BA08AC4708802A15C43ACC87BA",
                   "data_fsize": 612742384,
                   "data_psize": 1392,
                   "data_ppc": 64,
                   "data_cppc": 1,
                   "start_bitrate": 10000000,
                   "limit_bitrate": 20000000,
                   "avg_bitrate": 4098611}


