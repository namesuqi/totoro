# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from hamcrest import *
from libs.database.redis_single import redis_single_get_zset
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.push_hub.const import *

import copy
import json

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/push-hub-srv_api#2
    接口说明: courier向push-hub下发删除任务
    请求参数说明:
        file_id: 文件唯一标识符, 128位UUID组成
        priority: 任务的优先级 (优先级从高到低为 0, 1, 2, ...)
        push_id: vod-push的唯一标识, vod-push初始化时获取的mac地址
        push_ip: vod-push的ip
    请求体:
        [{task1}, {task2}, ...]
    返回体:
        {
            "task_count": Number,  # 收到的task数目
            "success_count": Number  # 执行成功(成功根据push_srv_ip插入到redis中)的task个数
        }

"""

# -------------------------------------------------------------------------------------------------------------


@given('prepare valid request body of delete_tasks')
def defaults_delete_tasks(context):
    context.delete_tasks = []

# -------------------------------------------------------------------------------------------------------------


@given('prepare a valid task for delete_tasks, push_id is {push_id}')
def defaults_task_info_of_delete_tasks(context, push_id):
    if push_id.upper() == "PUSH_ID":
        push_id = PUSH_ID

    context.task_info = {
        "file_id": context.file_id,
        "priority": PRIORITY,
        "push_id": push_id,
        "push_ip": PUSH_IP
    }


@given('add the task to delete_tasks')
def add_task_info_to_delete_tasks(context):
    context.delete_tasks.append(copy.deepcopy(context.task_info))


@given('add {count} tasks to delete_tasks with different file_id')
def add_many_task_info(context, count):
    for i in range(int(count)):
        context.task_info["file_id"] = "F" * 16 + str(i + 1).zfill(16)
        context.delete_tasks.append(copy.deepcopy(context.task_info))

# -------------------------------------------------------------------------------------------------------------


@when('push-hub receive the delete_tasks request')
def send_delete_tasks(context):

    uri = "/delete_tasks"
    body_data = context.delete_tasks

    context.response = send_http_request(
        POST,
        PUSH_HUB_HOST,
        PUSH_HUB_PORT,
        uri,
        HEADERS,
        None,
        body_data
    )

# -------------------------------------------------------------------------------------------------------------


@then("delete_task in PSPFC_{push_id} should be correct")
def verify_pspfc_is_correct(context, push_id):
    if push_id.upper() == "PUSH_ID":
        push_id = PUSH_ID
    request_tasks = [{"file_id": task["file_id"], "operation": "delete", "priority": task["priority"]}
                     for task in context.delete_tasks if task["push_id"] == push_id]
    redis_value = redis_single_get_zset("PSPFC_{0}".format(push_id))
    actual_tasks = [json.loads(task) for task in redis_value]
    print "task in redis:", actual_tasks
    print "task should be:", request_tasks
    assert_that(actual_tasks.sort(), equal_to(request_tasks.sort()), "value in PSPFC may be incorrect")

# -------------------------------------------------------------------------------------------------------------
