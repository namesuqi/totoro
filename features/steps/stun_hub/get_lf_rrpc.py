# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from hamcrest import *
from libs.request.http_request import *
from libs.request.http_method import *
from libs.database.redis_single import redis_single_add_list, redis_single_check_exists
from features.steps.stun_hub.const import *

import copy
import json

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/stun-hub-srv_doc#1-3-fetch-rrpc-cmd-req
    接口说明: stun-srv向stun-hub请求获取rrpc任务
    返回体:
        {
            "cmd": "distribute_task"
            "peer_ids": [peer_id]
            "task": "[{task1}, {task2}]"  # tasks in RRPC_<stun_ip> in redis-single
        }

"""

# -------------------------------------------------------------------------------------------------------------


@given("prepare an empty tasks_info")
def empty_tasks_info(context):
    context.tasks_info = {}


@given("prepare a valid download_task for get_lf_rrpc")
def defaults_of_download_task(context):
    context.task_info = {
        "file_id": context.file_id,
        "operation": OP_DOWNLOAD,
        "fsize": FSIZE,
        "psize": PSIZE,
        "ppc": PPC,
        "cppc": CPPC,
        "priority": PRIORITY,
        "port": PUSH_PORT,
        "server": PUSH_HOST,
        "peer_id": context.peer_id
    }


@given("prepare a valid delete_task for get_lf_rrpc")
def defaults_of_delete_task(context):
    context.task_info = {
        "file_id": context.file_id,
        "operation": OP_DELETE,
        "fsize": FSIZE,
        "psize": PSIZE,
        "ppc": PPC,
        "cppc": CPPC,
        "priority": PRIORITY,
        "port": PUSH_PORT,
        "server": PUSH_HOST,
        "peer_id": context.peer_id
    }


@given("add the task to tasks_info")
def save_task(context):
    task = copy.deepcopy(context.task_info)
    peer_id = task["peer_id"]
    if peer_id not in context.tasks_info.keys():
        context.tasks_info[peer_id] = [task]
    else:
        context.tasks_info[peer_id].append(task)


@given("add tasks_info to RRPC_{stun_ip} converged by peer_id")
def add_task_info_to_redis(context, stun_ip):
    if stun_ip.upper() == "STUN_IP":
        stun_ip = GET_LF_RRPC_STUN_IP
    redis_key = "RRPC_{0}".format(stun_ip)

    print "tasks:", context.tasks_info
    for peer_id, tasks in context.tasks_info.items():
        rrpc_command = {"cmd": CMD_DISTRIBUTE_TASK, "peer_ids": [peer_id], "task": json.dumps(tasks)}
        redis_single_add_list(redis_key, rrpc_command)

# -------------------------------------------------------------------------------------------------------------


@when("stun-hub receive the get_lf_rrpc request")
def send_get_lf_rrpc(context):

    uri = "/lf_rrpc"

    context.response = send_http_request(
        GET,
        STUN_HUB_HOST,
        STUN_HUB_PORT,
        uri,
        HEADERS,
        None,
        {}
    )

# -------------------------------------------------------------------------------------------------------------


@then("stun-hub should return correct rrpc_command")
def verify_response_data(context):
    rsp = context.response.json()
    assert_that(rsp["cmd"], equal_to(CMD_DISTRIBUTE_TASK))
    assert_that(len(rsp["peer_ids"]), equal_to(1))
    assert_that(json.loads(rsp["task"]), equal_to(context.tasks_info[rsp["peer_ids"][0]]))


@then("stun-hub should delete the RRPC_{stun_ip}")
def verify_rrpc_be_deleted(context, stun_ip):
    if stun_ip.upper() == "STUN_IP":
        stun_ip = GET_LF_RRPC_STUN_IP
    redis_key = "RRPC_{0}".format(stun_ip)
    assert_that(redis_single_check_exists(redis_key), equal_to(False))

# -------------------------------------------------------------------------------------------------------------

# @Given("peer id list is {invalid}")
# def generate_peer_id_list(context, invalid):
#     context.peer_ids = []
#     if invalid == 'correct':
#         context.peer_ids.append(PEER_ID1)
#         print '1231231231231312312'
#     elif invalid == 'missing':
#         pass
#     else:
#         context.peer_ids.append(invalid)
#
#
# @Given('peer ids list is {invalid}')
# def generate_peer_ids_list(context, invalid):
#     context.peer_ids = [PEER_ID1, PEER_ID2, PEER_ID3]
#     if invalid == 'correct':
#         pass
#     else:
#         context.peer_ids.append(invalid)
#
#
# @Given('peer ids are {all_} listed')
# def peers_login(context, all_):
#     peer_ids = context.peer_ids
#     if all_ == 'all':
#         for peer_id in peer_ids:
#             redis_cluster_setex_pnic("600", peer_id, VERSION, NAT_TYPE, PUBLIC_IP, PUBLIC_PORT, PRIVATE_IP,
#                                      PRIVATE_PORT, PROVINCE_ID_1, ISP_100017, CITY_ID, STUN_IP)
#         # time.sleep(5)
#     elif all_ == 'part':
#         for peer_id in peer_ids[:-1]:
#             redis_cluster_setex_pnic("600", peer_id, VERSION, NAT_TYPE, PUBLIC_IP, PUBLIC_PORT, PRIVATE_IP,
#                                      PRIVATE_PORT, PROVINCE_ID_1, ISP_100017, CITY_ID, STUN_IP)
#         # time.sleep(5)
#     elif all_ == 'not':
#         pass
#     print rc.exists('PNIC_'+PEER_ID1)
#     print rc.exists('PNIC_'+PEER_ID2)
#     print rc.exists('PNIC_'+PEER_ID3)
#
#
# @Given('file url is {invalid}')
# def generate_file_url(context, invalid):
#
#     if invalid == 'correct':
#         context.file_url = FILE_URL
#     elif invalid == 'missing':
#         context.file_url = ''
#     else:
#         context.file_url = invalid
#
#
# @Given('file id is {invalid}')
# def generate_file_id(context, invalid):
#
#     if invalid == 'correct':
#         context.file_id = FILE_ID
#     elif invalid == 'missing':
#         context.file_id = ''
#     else:
#         context.file_id = invalid
#
#
# @When('send join LF request')
# def send_join_lf_request(context):
#     context.response = hub_join_lf(HTTP, STUN_HUB_HOST, STUN_HUB_PORT, context.file_id, context.file_url,
#                                    context.peer_ids)
#
#
# @When('send leave lf request')
# def send_leave_lf_request(context):
#     context.response = hub_leave_lf(HTTP, STUN_HUB_HOST, STUN_HUB_PORT, context.file_id, context.peer_ids)
#
#
# @When('send hub lf rrpc request')
# def send_lf_rrpc(context):
#     context.response = hub_lf_rrpc(HTTP, STUN_HUB_HOST, STUN_HUB_PORT)
#
#
# @Given('the rrpc list contains {oder}')
# def prepare_rrpc_list(context, oder):
#
#     if oder == 'nothing':
#         pass
#
#     elif oder == 'one join LF oder':
#         context.execute_steps(u"""
#                 When send join LF request
#                 Then the response status code is 200
#                 """)
#
#     elif oder == 'one leave LF oder':
#         context.execute_steps(u"""
#                 When send leave LF request
#                 Then the response status code is 200
#                 """)
#
#     elif oder == 'two join LF oder and one leave LF oder':
#         context.execute_steps(u"""
#                 When send join LF request
#                 Then the response status code is 200
#                 """)
#         context.execute_steps(u"""
#                 When send leave LF request
#                 Then the response status code is 200
#                 """)
#         context.execute_steps(u"""
#                 When send join LF request
#                 Then the response status code is 200
#                 """)
#
#
# @Given('the oder contains {peer}')
# def prepare_peer_list(context, peer):
#     if peer == 'single peer':
#         context.execute_steps(u"""
#                 Given peer id list is correct
#                 And peer ids are all listed
#                 And file id is correct
#                 And file url is correct
#                 """)
#
#     elif peer == 'multi peer':
#         context.execute_steps(u"""
#                 Given peer ids list is correct
#                 And file id is correct
#                 And file url is correct
#                 """)
#
#
# def hub_lf_rrpc(protocol, host, port):
#     """
#     stun向stun-hub发送获取雷锋的rrpc请求
#     :param protocol:
#     :param host:
#     :param port:
#     :return:
#     """
#
#     url = "/lf_rrpc"
#
#     headers = HeaderData().Content__Type('application/json').ACCEPT('application/json').get_res()
#
#     response = send_request(
#         protocol,
#         GET,
#         host,
#         port,
#         url,
#         headers,
#         None,
#         {}
#     )
#     return response
#
#
# def hub_join_lf(protocol, host, port, file_id="", file_url="", peer_ids=""):
#     """
#     向stun-hub发送拉入雷锋的请求
#     :param protocol:
#     :param host:
#     :param port:
#     :param file_id:
#     :param file_url:
#     :param peer_ids:
#     :return:
#     """
#
#     url = "/join_lf"
#
#     headers = HeaderData().Content__Type('application/json').ACCEPT('application/json').get_res()
#
#     if type(peer_ids) != list:
#         peer_ids = [peer_ids]
#
#     body_data = {
#         "file_id": file_id,
#         "file_url": file_url,
#         "peer_ids": peer_ids
#     }
#
#     response = send_request(
#         protocol,
#         POST,
#         host,
#         port,
#         url,
#         headers,
#         None,
#         body_data
#     )
#     return response
#
#
# def hub_leave_lf(protocol, host, port, file_id="", peer_ids=""):
#     """
#     向stun-hub发送清退雷锋的请求
#     :param protocol:
#     :param host:
#     :param port:
#     :param file_id:
#     :param peer_ids:
#     :return:
#     """
#
#     url = "/leave_lf"
#
#     headers = HeaderData().Content__Type('application/json').ACCEPT('application/json').get_res()
#
#     if type(peer_ids) != list:
#         peer_ids = [peer_ids]
#
#     body_data = {
#         "file_id": file_id,
#         "peer_ids": peer_ids
#     }
#
#     response = send_request(
#         protocol,
#         POST,
#         host,
#         port,
#         url,
#         headers,
#         None,
#         body_data
#     )
#     return response
