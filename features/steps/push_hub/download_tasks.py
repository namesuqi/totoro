# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from hamcrest import *
from libs.database.redis_single import redis_single_get_zset, redis_single_delete_key
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.push_hub.const import *

import copy
import json

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/push-hub-srv_api#1
    接口说明: courier向push-hub下发下载任务
    请求参数说明:
        file_id: 文件唯一标识符, 128位UUID组成
        file_url: vod-push下载文件地址
        file_size: 文件大小, 单位Byte
        file_type: 文件类型, "bigfile"或"m3u8" (不限定值)
        ppc: 每个chunk的piece数
        cppc: 暂不使用
        piece_size: 每个piece data部分大小（不包含checksum与piece index）
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


@given('prepare valid request body of download_tasks')
def defaults_download_tasks(context):
    context.download_tasks = []

# -------------------------------------------------------------------------------------------------------------


@given('prepare a valid task for download_tasks, push_id is {push_id}')
def defaults_task_info_of_download_tasks(context, push_id):
    if push_id.upper() == "PUSH_ID":
        push_id = PUSH_ID

    context.task_info = {
        "file_id": context.file_id,
        "file_url": FILE_URL,
        "file_size": FILE_SIZE,
        "file_type": FILE_TYPE_BIGFILE,
        "ppc": PPC,
        "cppc": CPPC,
        "piece_size": PIECE_SIZE,
        "priority": PRIORITY,
        "push_id": push_id,
        "push_ip": PUSH_IP
    }


@given('add the task to download_tasks')
def add_task_info_to_download_tasks(context):
    context.download_tasks.append(copy.deepcopy(context.task_info))


@given('add {count} tasks to download_tasks with different file_id')
def add_many_task_info(context, count):
    for i in range(int(count)):
        context.task_info["file_id"] = "F" * 16 + str(i + 1).zfill(16)
        context.download_tasks.append(copy.deepcopy(context.task_info))

# -------------------------------------------------------------------------------------------------------------


@when('push-hub receive the download_tasks request')
def send_download_tasks(context):

    uri = "/download_tasks"
    body_data = context.download_tasks

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


@then("there should be {task_count} tasks in PSPFC_{push_id}")
def verify_pspfc_in_redis(context, task_count, push_id):
    redis_value = redis_single_get_zset(get_pspfc_key(push_id))
    print "task_count in redis:", len(redis_value), "task in redis:", redis_value
    assert_that(len(redis_value), equal_to(int(task_count)))


@then("push-hub should not add any task to PSPFC_{push_id}")
def verify_pspfc_is_empty(context, push_id):
    redis_value = redis_single_get_zset(get_pspfc_key(push_id))
    assert_that(len(redis_value), equal_to(0))


@then("download_task in PSPFC_{push_id} should be correct")
def verify_pspfc_is_correct(context, push_id):
    if push_id.upper() == "PUSH_ID":
        push_id = PUSH_ID

    request_tasks = []
    for task in context.download_tasks:
        if task.get("push_id", None) == push_id:
            task.pop("push_ip", None)
            task.pop("push_id", None)
            task["operation"] = "download"
            request_tasks.append(task)

    redis_value = redis_single_get_zset("PSPFC_{0}".format(push_id))
    actual_tasks = [json.loads(task) for task in redis_value]
    print "task in redis:", actual_tasks
    print "task should be:", request_tasks

    assert_that(actual_tasks.sort(), equal_to(request_tasks.sort()), "value in PSPFC may be incorrect")

# -------------------------------------------------------------------------------------------------------------


@given("clear PSPFC_{push_id}")
def delete_extra_pspfc(context, push_id):
    context.delete_key = push_id
    redis_single_delete_key(get_pspfc_key(context.delete_key))

# -------------------------------------------------------------------------------------------------------------


def get_pspfc_key(push_id):
    if push_id.upper() == "PUSH_ID":
        push_id = PUSH_ID
    return "PSPFC_{0}".format(push_id)

