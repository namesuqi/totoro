# coding=utf-8
# author: zengyuetian

from features.host import *

# -------------------------------------------------------------------------------------------------------------

TS_HOST = global_env.get(run_env, domains)["TS_HOST"]
TS_PORT = global_env.get(run_env, domains)["TS_PORT"]

# TS_HOST = "172.30.0.18"  # "ts.crazycdn.com"
# TS_PORT = 9510

# SEEDS_HOST = "seeds.crazycdn.com"
# SEEDS_PORT = 80

# -------------------------------------------------------------------------------------------------------------

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/4.2.0"
}

# -------------------------------------------------------------------------------------------------------------

PREFIX = "FFFFFFFF"
PREFIX_HIWIFI = "075BCE1A"

VERSION = "4.2.0"
MIN_VERSION = "4.1.0"

STUN_IP = "192.168.1.1"

NAT_TYPE = 1
NAT_TYPE_HIWIFI = 3

PUBLIC_IP = "116.231.167.180"  # isp: 100017
PUBLIC_PORT = 56659
PRIVATE_IP = "192.168.1.2"
PRIVATE_PORT = 56659

ISP_100017 = "100017"
ISP_ID_100017 = "100017"
PROVINCE_ID_310000 = "310000"
CITY_ID_310100 = "310100"

MACS = {"name": "win2", "addr": "00:50:56:C0:00:08"}

TTL = 300  # for redis-PNIC

# -------------------------------------------------------------------------------------------------------------

CPPC = 1

PPC = 304

PSIZE = 1392

FSIZE_1G = 1024*1024*1024

PERCENT_0 = 0
PERCENT_100 = 100

STAT_DOWNLOADING = "downloading"
STAT_INTERRUPT = "interrupt"
STAT_DONE = "done"
STAT_WAITING = "waiting"
STAT_DELETED = "deleted"
# STAT_NONE = "none"  # 0.0.15版本以下

DISK_1G = 1024*1024*1024
LSM_1G = 1024*1024*1024
LSM_200M = 200*1024*1024

UNIVERSE_TRUE = True
UNIVERSE_FALSE = False

DURATION = 600

DOWNLOAD_1G = 1024*1024*1024
PROVIDE_1G = 1024*1024*1024

TYPE_VOD = "vod"

OP_ADD = "add"
OP_DEL = "del"
OP_PLAYING = "playing"

CDN_1G = 1024*1024*1024
P2P_2G = 2*1024*1024*1024

P2PENABLE_TRUE = True
P2PENABLE_FALSE = False

ERROR_NO = ""
ERROR_DECODE_FAIL = "E_DECODE_FAIL"

# -------------------------------------------------------------------------------------------------------------

# TBD
PEER_ID1 = "0000073012345123451234512345AAAA"

STUN_IP1 = "123.56.30.51"

PROVINCE_ID_1 = "310"

CITY_ID = "123"

SLICE_ID = 63

CHUNK_ID_NORMAL = 20000

PLAY_TYPE_FLV = "live_flv"
PLAY_TYPE_TS = "live_ts"
PLAY_TYPE_M3U8 = "live_m3u8"
PLAY_TYPE_INVALID = "invalid"

TIMESTAMP_NOW = "now_time"  # peer_live_progress函数参数report_time="now_time"时，会按当前时间戳重新赋值

UUID_INVALID_1 = "*--"  # 无效参数
UUID_INVALID_2 = "343855B7C23B4C349AFFED0D3B5EC73"  # 31位
UUID_INVALID_3 = "343855B7C23B4C349AFFED0D3B5EC73DA"  # 33位
UUID_INVALID_4 = "343855B7C23B4C349AFFED0D3B5EHZZG"  # 32位非十六进制
UUID_INVALID_5 = "4EB5897E90DA45ACAC38576EAD7786A54EB5897E90DA45ACAC38576EAD7786A54EB5897E90DA45ACAC3857"
UUID_INVALID_LIST = [UUID_INVALID_1, UUID_INVALID_2, UUID_INVALID_3, UUID_INVALID_4, UUID_INVALID_5]


# invalid
UUID_INVALID_A = ""  # 无效参数
UUID_INVALID_B = "2222222C23B4C349AFFED0D3B5EC7FF"  # 31位
UUID_INVALID_C = "343855B7C23B4C349AFFED0D3B5EC73DA"  # 33位
UUID_INVALID_D = "343855B7C23B4C349AFFED0D3B5EHZZG"  # 32位非十六进制
UUID_INVALID_E = "4EB5897E90DA45ACAC38576EAD7786A54EB5897E90DA45ACAC38576EAD7786A54EB5897E90DA45ACAC3857"
UUID_INVALID_F = "A"  # 1位
UUID_INVALID_NULL = ""
UUID_INVALID_Form = [UUID_INVALID_A, UUID_INVALID_B, UUID_INVALID_C, UUID_INVALID_D, UUID_INVALID_E,UUID_INVALID_F]

# -------------------------------------------------------------------------------------------------------------


