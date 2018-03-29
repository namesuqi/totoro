# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from hamcrest import *
from libs.database.redis_single import redis_single_get_list, redis_single_delete_key
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.stun_hub.const import *

import copy
import json

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/stun-hub-srv_doc#1-1-push-distribute-task-req
    接口说明: courier向stun-hub下发rrpc任务
    请求参数说明:
        file_id: 文件唯一标识符, 128位UUID组成
        operation: "download"或"delete"（强匹配）
        fsize: 文件大小, 单位Byte
        ppc: 每个chunk的piece数
        cppc: 暂不使用
        priority: 任务的优先级 (优先级从高到低为 0, 1, 2, ...)
        port: vod-push的port
        server: vod-push的host
        peer_id: 节点唯一标识符, 128位UUID组成
    请求体:
        [{task1}, {task2}, ...]
    返回体:
        {"succ_task_count": 成功下发任务数}

"""

# -------------------------------------------------------------------------------------------------------------


@given("prepare valid request body of distribute_task")
def create_request_body(context):
    context.distribute_task = []
    context.rrpc_tasks = []

# -------------------------------------------------------------------------------------------------------------


@given("prepare a valid task for distribute_task")
def create_task_info(context):
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


@given("add task_info to distribute_task")
def add_task_info_to_tasks(context):
    task_info = copy.deepcopy(context.task_info)
    context.distribute_task.append(task_info)

    peer_id = task_info.get("peer_id", "unknown_peer_id")
    stun_ip = context.pnic.get(peer_id, "unknown_stun_ip")
    context.rrpc_tasks.append((stun_ip, peer_id, task_info))

# -------------------------------------------------------------------------------------------------------------


@when("stun-hub receive the distribute_task request")
def send_request(context):

    uri = "/distribute_task"
    body_data = context.distribute_task

    context.response = send_http_request(
        POST,
        STUN_HUB_HOST,
        STUN_HUB_PORT,
        uri,
        HEADERS,
        None,
        body_data
    )

# -------------------------------------------------------------------------------------------------------------


@then("there should be {count} rrpc_commands in RRPC_{stun_ip}")
def verify_rrpc_in_redis(context, count, stun_ip):
    redis_value = get_rrpc_commands(stun_ip)
    print "rrpc_commands should be", context.rrpc_tasks
    assert_that(len(redis_value), equal_to(int(count)))


@then("rrpc_command in RRPC_{expect_stun_ip} should be correct")
def verify_rrpc_is_correct(context, expect_stun_ip):
    if expect_stun_ip.upper() == "STUN_IP":
        expect_stun_ip = STUN_IP
    expect_rrpc_commands = {}
    for stun_ip, peer_id, task in context.rrpc_tasks:
        if stun_ip == expect_stun_ip:
            if peer_id not in expect_rrpc_commands:
                expect_rrpc_commands[peer_id] = [task]
            else:
                expect_rrpc_commands[peer_id].append(task)
    print "tasks should be:", expect_rrpc_commands

    redis_value = redis_single_get_list("RRPC_{0}".format(expect_stun_ip))
    print "task in redis:", redis_value
    for actual_rrpc_command in redis_value:
        actual_rrpc_command = json.loads(actual_rrpc_command)
        assert_that(actual_rrpc_command["cmd"], equal_to(CMD_DISTRIBUTE_TASK))
        assert_that(len(actual_rrpc_command["peer_ids"]), equal_to(1), "peer_ids should be [peer_id]")
        rrpc_peer_id = actual_rrpc_command["peer_ids"][0]
        assert_that(json.loads(actual_rrpc_command["task"]), equal_to(expect_rrpc_commands[rrpc_peer_id]), "task error")

# -------------------------------------------------------------------------------------------------------------


@given('clear RRPC_{stun_ip}')
def clear_rrpc(context, stun_ip):
    if stun_ip.upper() == "STUN_IP":
        stun_ip = STUN_IP
    context.redis_key = "RRPC_{0}".format(stun_ip)
    redis_single_delete_key(context.redis_key)

# -------------------------------------------------------------------------------------------------------------


def get_rrpc_commands(stun_ip):
    if stun_ip.upper() == "STUN_IP":
        stun_ip = STUN_IP
    redis_key = "RRPC_{0}".format(stun_ip)
    redis_value = redis_single_get_list(redis_key)
    print redis_key, "-- count:", len(redis_value), "; value:", redis_value
    return redis_value  # ['{}', '{}']

# -------------------------------------------------------------------------------------------------------------

# @given(u'there is {num:Number} seed task')
# def there_is_seed_task(context, num):
#     context.tasks = list()
#     context.tasks.append(update_task_peer_id(VALID_DOWNLOAD_TASK, context.peer_id))
#     if num == 2:
#         context.tasks.append(update_task_peer_id(VALID_DELETE_TASK, context.peer_id))
#
#
# @given(u'there is {num:Number} invalid seed task')
# def there_is_invalid_seed_task(context, num):
#     context.tasks = list()
#     context.tasks.append(INVALID_DOWNLOAD_TASK)
#     if num == 2:
#         context.tasks.append(INVALID_DELETE_TASK)
#
#
# @given(u'there is {num1:Number} valid seed task {num2:Number} invalid seed task')
# def there_is_valid_invalid_seed_task(context, num1, num2):
#     context.tasks = list()
#     context.tasks.append(INVALID_DOWNLOAD_TASK)
#     context.tasks.append(VALID_DOWNLOAD_TASK)
#     if num1 == 2:
#         context.tasks.append(VALID_DELETE_TASK)
#     if num2 == 2:
#         context.tasks.append(INVALID_DELETE_TASK)


# @when(u'send the task to stun-hub')
# def send_the_task_to_stun_hub(context):
#     context.response = distribute_task(STUN_HUB_HOST, STUN_HUB_PORT, context.tasks)
#
#
# @then(u'the response task count is {count:Number}')
# def response_task_count_is(context, count):
#     real_count = context.response.json().get('succ_task_count', 'None')
#     print("expected successful count is {0}".format(count))
#     print("real successful count is {0}".format(real_count))
#     assert real_count == count
#
#
# def distribute_task(host, port, tasks):
#     """
#     策略向stub-hub发送任务请求
#     :param host:服务器
#     :param port:端口
#     :param tasks:task list
#     :return: http response
#     """
#
#     url = "/distribute_task"
#
#     headers = HeaderData().Content__Type('application/json').ACCEPT('application/json').get_res()
#     body_data = tasks
#
#     response = send_http_request(
#         POST,
#         host,
#         port,
#         url,
#         headers,
#         None,
#         body_data
#     )
#
#     return response







