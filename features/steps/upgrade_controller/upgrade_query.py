# coding=utf-8
# __author__ = 'liwenxuan'
# 放置和同名feature文件相关的测试步骤

from behave import given, when, then
from hamcrest import assert_that, equal_to
from libs.request.http_request import send_http_request
from libs.request.http_method import POST
from features.steps.upgrade_controller.const import *

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/p2pserver/p2pserver/wikis/upgrade-controller#1-1-upgrade-query-request
    接口说明: SDK开机时, 向upgrade_controller查询是否需要升级
    请求参数说明:
        (1) 若SDK无core文件
        | field     | type     | limit range     | description     |
        | is_basic  | string   | "true", "false" |                 |

        (2) 若SDK有core文件, 且NAT探测成功(成功获取到public_ip)
        | field     | type     | limit range     | description                |
        | peer_id   | string   | 三十二位十六进制 | 设备唯一标识符, 128位UUID   |
        | version   | string   | A.B.C           | SDK版本号                   |
        | public_ip | string   | ip              |                            |

        (3) 若SDK有core文件, 但NAT探测失败(没有获取到public_ip)
        | field     | type     | limit range     | description                |
        | peer_id   | string   | 三十二位十六进制 | 设备唯一标识符, 128位UUID   |
        | version   | string   | A.B.C           | SDK版本号                   |
        | public_ip | string   | ""              |                            |
    返回体:
        {"target_version": upgrade_version}  # 不需要升级时, 返回的version为""

"""

# -------------------------------------------------------------------------------------------------------------


@given('prepare a valid upgrade_query request without core')
def create_request_body(context):
    context.upgrade_query = {
        "is_basic": IS_BASIC_TRUE
    }


@given('prepare a valid upgrade_query request with core and success of nat_detect')
def create_request_body(context):
    context.upgrade_query = {
        "peer_id": context.peer_id,
        "version": SDK_VERSION,
        "public_ip": PUBLIC_IP
    }
    # if context.text:
    #     context.upgrade_query.update(eval(context.text))


@given('prepare a valid upgrade_query request with core and failure of nat_detect')
def create_request_body(context):
    context.upgrade_query = {
        "peer_id": context.peer_id,
        "version": SDK_VERSION,
        "public_ip": ""
    }
    # if context.text:
    #     context.upgrade_query.update(eval(context.text))

# -------------------------------------------------------------------------------------------------------------


@when('upgrade_controller receive the upgrade_query request')
def send_request(context):

    uri = "/upgrade_query"
    body_data = context.upgrade_query

    context.response = send_http_request(
        POST,
        UPGRADE_CONTROLLER_HOST,
        UPGRADE_CONTROLLER_PORT,
        uri,
        HEADERS,
        None,
        body_data
    )

# -------------------------------------------------------------------------------------------------------------


@then('upgrade_query response should be "{response_data}"')
def verify_that_response_data_is_correct(context, response_data):
    actual_result = context.response.json()
    assert_that(actual_result.keys(), equal_to(["target_version"]))

    actual_target_version = actual_result.get("target_version", None)
    expect_target_version = eval(response_data).get("target_version", None)
    if expect_target_version == "TARGET_VERSION":
        expect_target_version = TARGET_VERSION
    assert_that(actual_target_version, equal_to(expect_target_version), "unexpected target_version")

# -------------------------------------------------------------------------------------------------------------


@given('make sure that there is no rule in upgrade_controller')
def send_empty_upgrade_rule(context):
    context.execute_steps(u"""
        Given prepare an empty upgrade_rule request
        When upgrade_controller receive the upgrade_rule request
        Then response status_code should be 200
        And response error_code should be None
        And upgrade_rule response should be "{"result": "OK"}"
    """)


@given('make sure that there is a rule valid for all in upgrade_controller')
def send_valid_upgrade_rule(context):
    context.execute_steps(u"""
        Given prepare an empty upgrade_rule request
        And prepare a rule_group without rules
        And prepare a rule
        And add the rule to rule_group
        And add the rule_group to upgrade_rule
        When upgrade_controller receive the upgrade_rule request
        Then response status_code should be 200
        And response error_code should be None
        And upgrade_rule response should be "{"result": "OK"}"
    """)

# -------------------------------------------------------------------------------------------------------------



