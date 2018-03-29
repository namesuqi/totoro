# coding=utf-8
# __author__ = 'liwenxuan'
# 放置和同名feature文件相关的测试步骤

from behave import given, when, then
from hamcrest import assert_that, equal_to
from libs.request.http_request import send_http_request
from libs.request.http_method import POST
from features.steps.upgrade.const import *

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/p2pserver/p2pserver/wikis/upgrade_srv
    接口说明: SDK向upgrade-srv获取升级版本的路径
    请求参数说明:
        "targetversion": "4.1.0",//目标版本，必选
        "peerid":"0000000418874D798552C9AF05CE55B0",//peer id， 可选
        "shellversion": "1.0.1",//shell版本，必选
        "os": "linux",//操作系统类型，必选
        "osversion": "1.0.1",//操作系统版本，必选
        "distribution": "ubuntu",//操作系统发行版，必选
        "distributionversion": "1.0.1",//发行版版本，必选
        "envCPU": "x86_64",//cpu，必选
        "realCPU": "x86_64",//，必选
        "toolchain": "nocheck"//工具链，必选
    返回体:
        {
            "targetversion": "4.1.0",//目标版本，必选
            "md5": "da17695483a955008d2430668b093eb4",//文件md5
            "url": "http://127.0.0.1/libys-core.4.1.0.so"//新版采用download srv ip与文件路径拼接而成
        }

"""

# -------------------------------------------------------------------------------------------------------------

# upgrade_get涉及mongo_db的部分尚未完成(setup, teardown和data_check)

# -------------------------------------------------------------------------------------------------------------


@given('prepare a valid upgrade_get request')
def create_request_body(context):
    context.upgrade_get = {
        "targetversion": TARGET_VERSION,
        "peerid": context.peer_id,
        "shellversion": SHELL_VERSION,
        "os": OS_LINUX,
        "osversion": OS_VERSION,
        "distribution": DISTRIBUTION_CENTOS,
        "distributionversion": DISTRIBUTION_VERSION,
        "envCPU": ENV_CPU,
        "realCPU": REAL_CPU,
        "toolchain": TOOLCHAIN
    }

# -------------------------------------------------------------------------------------------------------------


@when('upgrade-srv receive the upgrade_get request')
def send_request(context):

    uri = "/upgrade_get"
    body_data = context.upgrade_get

    context.response = send_http_request(
        POST,
        UPGRADE_HOST,
        UPGRADE_PORT,
        uri,
        HEADERS,
        None,
        body_data
    )

# -------------------------------------------------------------------------------------------------------------


@then('response data of upgrade_get should be correct')
def verify_that_response_data_is_correct(context):
    actual_result = context.response.json()
    assert_that(actual_result.get("errcode", None), equal_to(""), "errcode should be empty")
    # assert_that(actual_result.get("targetversion", None), equal_to(expect_target_version), "unexpected targetversion")  # involved by mongo_db
    # assert_that(actual_result.get("md5", None), equal_to(expect_md5), "unexpected md5")  # involved by mongo_db
    # assert_that(actual_result.get("url", None), equal_to(expect_url), "unexpected url")  # involved by mongo_db


@then('response error_type of upgrade_get should be {error_type}')
def verify_that_response_data_is_correct(context, error_type):
    actual_result = context.response.json()
    assert_that(actual_result.get("errcode", None), equal_to(error_type), "unexpected errcode")
    assert_that(actual_result.get("targetversion", None), equal_to(""), "targetversion should be empty")
    assert_that(actual_result.get("md5", None), equal_to(""), "md5 should be empty")
    assert_that(actual_result.get("url", None), equal_to(""), "url should be empty")

# -------------------------------------------------------------------------------------------------------------

