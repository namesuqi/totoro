# coding=utf-8
# __author__ = 'liwenxuan'

from features.host import *

# -------------------------------------------------------------------------------------------------------------

UPGRADE_HOST = global_env.get(run_env, domains)["UPGRADE_HOST"]
UPGRADE_PORT = global_env.get(run_env, domains)["UPGRADE_PORT"]

# -------------------------------------------------------------------------------------------------------------

# 请求头信息
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/3.19.9"
}

# -------------------------------------------------------------------------------------------------------------

TARGET_VERSION = "4.1.0"

SHELL_VERSION = "1.0.1"

OS_LINUX = "linux"
OS_VERSION = "1.0.1"

DISTRIBUTION_UBUNTU = "ubuntu"
DISTRIBUTION_CENTOS = "centos"
DISTRIBUTION_VERSION = "1.0.1"

ENV_CPU = "x86_64"
REAL_CPU = "x86_64"

TOOLCHAIN = "nocheck"

# -------------------------------------------------------------------------------------------------------------



