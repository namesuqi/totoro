# coding=utf-8
# __author__ = 'liwenxuan'

from features.host import *

# -------------------------------------------------------------------------------------------------------------

DIR_HOST = global_env.get(run_env, domains)["DIR_HOST"]
DIR_PORT = global_env.get(run_env, domains)["DIR_PORT"]

# -------------------------------------------------------------------------------------------------------------

# request header
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/3.19.9",
}

# -------------------------------------------------------------------------------------------------------------

USER_CLOUTROPY = "cloutropy"
USER_CRAZYCDN = "crazycdn"

USER_NOT_EXIST = "auto_test"

TYPE_CDN = "CDN"
TYPE_OSS = "OSS"
TYPE_M3U8 = "M3U8"

DOMAIN_CLOUTROPY = "yunshang.cloutropy.com"
DOMAIN_CRAZYCDN = "yunshang.crazycdn.com"

URL_EXIST = "http://yunshang.cloutropy.com/demo/low/Ocean_2mbps.ts"

TABLE_FILES = "ppc_tenant_files"
TABLE_USERS = "ppc_tenants"

# -------------------------------------------------------------------------------------------------------------

# config: msg in MySQL for auto_test  # type(id) should be int, but string here
config = {
    USER_CLOUTROPY: {
        "tenant_id": "99903",
        "prefix": "FFFFFFFF",
        "source_id": {  # sid
            TYPE_OSS: "030101",
            TYPE_CDN: "030102",
            TYPE_M3U8: "030103"
        },
        "domain_id": {  # active_prefix_id
            DOMAIN_CLOUTROPY: "030201",
        },
    },
    USER_CRAZYCDN: {
        "tenant_id": "99904",
        "prefix": "FFFFFFF4",
        "source_id": {  # sid
            TYPE_OSS: "040101",
            TYPE_CDN: "040102",
            TYPE_M3U8: "040103"
        },
        "domain_id": {  # active_prefix_id
            DOMAIN_CRAZYCDN: "040201",
        },
    }
}

# -------------------------------------------------------------------------------------------------------------

SOURCE_ID = int(config[USER_CLOUTROPY]["source_id"][TYPE_CDN])
DOMAIN_ID = int(config[USER_CLOUTROPY]["domain_id"][DOMAIN_CLOUTROPY])

# -------------------------------------------------------------------------------------------------------------

