# coding=utf-8
# __author__ = 'liwenxuan'

from features.host import *

# -------------------------------------------------------------------------------------------------------------

UPGRADE_CONTROLLER_HOST = global_env.get(run_env, domains)["UPGRADE_CONTROLLER_HOST"]
UPGRADE_CONTROLLER_PORT = global_env.get(run_env, domains)["UPGRADE_CONTROLLER_PORT"]

# -------------------------------------------------------------------------------------------------------------

# 请求头信息
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/3.19.9"
}

# -------------------------------------------------------------------------------------------------------------

IS_BASIC_TRUE = "true"
IS_BASIC_FALSE = "false"

SDK_VERSION = "4.0.0"
# UPGRADE_VERSION = "4.2.10"
TARGET_VERSION = "4.2.10"

PUBLIC_IP = "192.168.1.1"

# -------------------------------------------------------------------------------------------------------------


