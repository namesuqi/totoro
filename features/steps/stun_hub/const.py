# coding=utf-8
# author: zengyuetian

from features.host import *
from features.steps.ts.const import STUN_IP

# -------------------------------------------------------------------------------------------------------------

STUN_HUB_HOST = global_env.get(run_env, domains)["STUN_HUB_HOST"]  # "172.30.0.25"  # "stun-hub.ys-internal.com"
STUN_HUB_PORT = global_env.get(run_env, domains)["STUN_HUB_PORT"]

# -------------------------------------------------------------------------------------------------------------

GET_LF_RRPC_STUN_IP = global_env[run_env]["JENKINS"]

# -------------------------------------------------------------------------------------------------------------

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/3.19.9"
}

# -------------------------------------------------------------------------------------------------------------

STUN_IP = STUN_IP

CPPC = "1"

PPC = "304"

PSIZE = "1392"

FSIZE = "775134238"

PRIORITY = "0"

PUSH_HOST = "push.crazycdn.com"
PUSH_PORT = "80"

OP_DOWNLOAD = "download"
OP_DELETE = "delete"

CMD_DISTRIBUTE_TASK = "distribute_task"
CMD_UPGRADE_TASK = "upgrade_task"

TARGET_VERSION = "5.0.0"

# -------------------------------------------------------------------------------------------------------------

# VALID_DELETE_TASK = {"file_id": "7FF5B13044EB44FBA4FAAA85F9400643",
#                      "operation": "delete",
#                      "fsize": "775134238",
#                      "psize": "864",
#                      "ppc": "368",
#                      "cppc": "1",
#                      "priority": "10",
#                      "port": "80",
#                      "server": "push.crazycdn.com",
#                      "peer_id": "0000000464C14A7C9B43FE95FA2DAF7B"}
#
# VALID_DOWNLOAD_TASK = {"file_id": "7FF5B13044EB44FBA4FAAA85F9400643",
#                        "operation": "download",
#                        "fsize": "775134238",
#                        "psize": "864",
#                        "ppc": "368",
#                        "cppc": "1",
#                        "priority": "10",
#                        "port": "80",
#                        "server": "push.crazycdn.com",
#                        "peer_id": "0000000464C14A7C9B43FE95FA2DAF7B"}
#
# INVALID_DOWNLOAD_TASK = dict(VALID_DOWNLOAD_TASK)
# INVALID_DOWNLOAD_TASK["peer_id"] = INVALID_DOWNLOAD_TASK["peer_id"] + "F"
#
# INVALID_DELETE_TASK = dict(VALID_DELETE_TASK)
# INVALID_DELETE_TASK["peer_id"] = INVALID_DELETE_TASK["peer_id"] + "F"
#
# # -------------------------------------------------------------------------------------------------------------
#
#
# def update_task_peer_id(task, peer_id):
#     task["peer_id"] = peer_id
#     return task
#
# if __name__ == "__main__":
#     task = update_task_peer_id(VALID_DOWNLOAD_TASK, "AAAA")
#     print task
