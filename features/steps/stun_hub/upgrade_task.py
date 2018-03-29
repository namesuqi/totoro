# coding=utf-8
# __author__ = 'liwenxuan'
# 放置和同名feature文件相关的测试步骤

from behave import *
from hamcrest import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.stun_hub.const import *
from features.steps.upgrade_controller.const import TARGET_VERSION
from features.steps.common import get_peer_id_distribution
from features.steps.stun_hub.distribute_task import get_rrpc_commands

from copy import deepcopy

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/devs/vod/ctrl-plane/stun-hub/#1-1-upgrade-task-req
    接口说明: upgrade_controller向stun-hub下发升级任务
    请求参数说明:
        target_version: 升级版本
        peer_ids: 由peer_id组成的list
    请求体:
        [{task1}, {task2}, ...]
    返回体:
        {"succ_task_count": 成功下发任务数}

"""

# -------------------------------------------------------------------------------------------------------------


@given("prepare an empty upgrade_task request")
def create_request_body(context):
    context.upgrade_task = []
    context.expect_upgrade_tasks = []


@given("prepare a valid task for upgrade_task")
def create_task_info(context):
    context.task_info = {
        "target_version": TARGET_VERSION,
        "peer_ids": []
    }


@given("add the peer_id to peer_ids of upgrade_task")
def add_peer_id_to_peer_ids(context):
    context.task_info["peer_ids"].append(deepcopy(context.peer_id))


@given("add the task to upgrade_task")
def add_task_info_to_tasks(context):
    task_info = deepcopy(context.task_info)
    context.upgrade_task.append(task_info)

    target_version = task_info["target_version"]
    for stun_ip, peer_ids in get_peer_id_distribution(context.pnic).items():
        context.expect_upgrade_tasks.append((stun_ip, peer_ids, target_version))

# -------------------------------------------------------------------------------------------------------------


@when("stun-hub receive the upgrade_task request")
def send_request(context):

    uri = "/upgrade_task"
    body_data = context.upgrade_task

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


@then("there should be {count} upgrade_tasks in RRPC_{stun_ip}")
def verify_rrpc_in_redis(context, count, stun_ip):
    redis_value = get_rrpc_commands(stun_ip)
    print "upgrade_tasks should be", context.upgrade_tasks
    assert_that(len(redis_value), equal_to(int(count)))


@then("upgrade_tasks in RRPC_{stun_ip} should be correct")
def verify_rrpc_is_correct(context, stun_ip):
    redis_value = get_rrpc_commands(stun_ip)
    print "task in redis:", redis_value

    # TO BE CONTINUED...
    # print "tasks should be:", expect_upgrade_tasks
    #
    # for actual_upgrade_task in redis_value:
    #     actual_upgrade_task = json.loads(actual_upgrade_task)
    #     assert_that(actual_upgrade_task["cmd"], equal_to(CMD_DISTRIBUTE_TASK))
    #     assert_that(len(actual_upgrade_task["peer_ids"]), equal_to(1), "peer_ids should be [peer_id]")
    #     rrpc_peer_id = actual_upgrade_task["peer_ids"][0]
    #     assert_that(json.loads(actual_upgrade_task["task"]), equal_to(expect_upgrade_tasks[rrpc_peer_id]), "task error")

# -------------------------------------------------------------------------------------------------------------






