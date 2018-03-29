# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from hamcrest import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.push_hub.const import *
from libs.database.redis_single import redis_single_add_zset, redis_single_check_exists, redis_single_get_zset

import time
import copy

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/push-hub-srv_api#3
    接口说明: vod-push向push-hub请求获取预处理任务列表(pspfc_task)
    请求参数说明:
        push_id: vod-push的id, vod-push初始化时获取的mac地址
    返回体:
        [{task1}, {task2}, ...]

"""

# -------------------------------------------------------------------------------------------------------------


@given('prepare valid request body of preprocessing_tasks, push_id defaults to {push_id}')
def defaults_preprocessing_tasks(context, push_id):
    if push_id.upper() == "PUSH_ID":
        push_id = PUSH_ID

    context.preprocessing_tasks = {
        "id": push_id,
    }

    context.pspfc_tasks = []

# -------------------------------------------------------------------------------------------------------------


@given('prepare a valid download_task')
def defaults_of_download_task(context):
    context.pspfc_task = {
        "file_id": context.file_id,
        "file_url": FILE_URL,
        "file_size": FILE_SIZE,
        "ppc": PPC,
        "cppc": CPPC,
        "piece_size": PIECE_SIZE,
        "operation": OP_DOWNLOAD,
        "priority": PRIORITY,
    }


@given('prepare a valid delete_task')
def defaults_of_delete_task(context):
    context.pspfc_task = {
        "file_id": context.file_id,
        "operation": OP_DELETE,
        "priority": PRIORITY
    }


@given('add task_info to PSPFC_{push_id} and set score to localtime{adjust_second}s')
def add_task_info_to_redis(context, push_id, adjust_second):
    if push_id.upper() == "PUSH_ID":
        push_id = PUSH_ID

    redis_key = "PSPFC_{0}".format(push_id)
    localtime = int(time.time())
    redis_single_add_zset(redis_key, localtime+int(adjust_second), context.pspfc_task)

    if int(adjust_second) > -180:
        valid_task = (push_id, copy.deepcopy(context.pspfc_task))
        context.pspfc_tasks.append(valid_task)

# -------------------------------------------------------------------------------------------------------------


@when('push-hub receive the preprocessing_tasks request')
def send_preprocessing_tasks(context):

    # record PSPFC status before sent request so that we can verify if push-hub do anything to PSPFC
    context.redis_key = "PSPFC_{0}".format(context.preprocessing_tasks.get("id", None))
    context.redis_value_before_request = redis_single_get_zset(context.redis_key)
    print context.redis_key, "before request:", context.redis_value_before_request

    uri = "/preprocessing_tasks?{0}"\
        .format("&".join(["{0}={1}".format(k, v) for k, v in context.preprocessing_tasks.items()]))

    context.response = send_http_request(
        GET,
        PUSH_HUB_HOST,
        PUSH_HUB_PORT,
        uri,
        HEADERS,
        None,
        {}
    )

# -------------------------------------------------------------------------------------------------------------


@then('response data of preprocessing_tasks should be all valid tasks in PSPFC_{expect_push_id}')
def verify_pspfc_and_response(context, expect_push_id):
    if expect_push_id.upper() == "PUSH_ID":
        expect_push_id = PUSH_ID
    print "all_valid_tasks:", context.pspfc_tasks
    valid_tasks = [valid_task for push_id, valid_task in context.pspfc_tasks if push_id == expect_push_id]
    valid_tasks.reverse()
    assert_that(context.response.json(), equal_to(valid_tasks))


@then('push-hub should delete PSPFC_{push_id}')
def verify_pspfc_be_deleted(context, push_id):
    if push_id.upper() == "PUSH_ID":
        push_id = PUSH_ID
    redis_key = "PSPFC_{0}".format(push_id)
    assert_that(redis_single_check_exists(redis_key), equal_to(False))


@then("push-hub should do nothing to the PSPFC")
def verify_pspfc_has_no_change(context):
    redis_value_after_request = redis_single_get_zset(context.redis_key)
    assert_that(redis_value_after_request, equal_to(context.redis_value_before_request))

# -------------------------------------------------------------------------------------------------------------



