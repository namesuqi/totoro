# coding=utf-8
# __author__ = 'liwenxuan'

from features.host import *

# -------------------------------------------------------------------------------------------------------------

PUSH_HUB_HOST = global_env.get(run_env, domains)["PUSH_HUB_HOST"]  # "172.30.0.35"
PUSH_HUB_PORT = global_env.get(run_env, domains)["PUSH_HUB_PORT"]

# -------------------------------------------------------------------------------------------------------------

SOURCE_IP = global_env.get(run_env, domains)["JENKINS"]
PUSH_IP = "192.168.1.1"

# -------------------------------------------------------------------------------------------------------------

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/3.19.9",
    # "x-forwarded-for": PUSH_IP,
}

# -------------------------------------------------------------------------------------------------------------

FILE_URL = "TEST"
FILE_SIZE = 775134238
FILE_TYPE_BIGFILE = "bigfile"
FILE_TYPE_M3U8 = "m3u8"

CPPC = 1
PPC = 304
PIECE_SIZE = 1392

PRIORITY = 0

PUSH_ID = "FF:FF:FF:FF:FF:FF"
PUSH_IP = PUSH_IP

OP_DOWNLOAD = "download"
OP_DELETE = "delete"

# if server_tag >= 0.0.15
NEED_AUTHORITY_YES = "yes"
NEED_AUTHORITY_NO = "no"

# -------------------------------------------------------------------------------------------------------------

# VALID_PUSH_IP = "172.30.254.150"



