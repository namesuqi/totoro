# coding=utf-8
# __author__ = 'liwenxuan'
# 放置和同名feature文件相关的测试步骤

from behave import given, when, then
from hamcrest import assert_that, equal_to
from libs.request.http_request import send_http_request
from libs.request.http_method import POST
from features.steps.upgrade_controller.const import *

from copy import deepcopy

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/p2pserver/p2pserver/wikis/upgrade-controller#2-1-upgrade-rule-request
    接口说明: opt-srv向upgrade_controller下发升级策略
    请求参数说明:
        user_ids: list, 该规则组对该范围内的prefix生效, 为空列表时表示全部
        province_ids: list, 该规则组对该范围内的province_id生效, 为空列表时表示全部
        isp_ids: list, 该规则组对该范围内的isp_id生效, 为空列表时表示全部
        # 升级规则组生效须同时满足上三条
        percent: float, 灰度升级占比
        upgrade_paths: list, 升级规则组, 可配置一个或多个
            core_version: [version1, version2], 该规则对该范围内的sdk_version生效(左右皆取到)
            target_version: 满足该规则时的升级版本
    请求体:
        body_data: [{rule_group}, {rule_group}]
        rule_group: {"user_ids": [], "province_ids": [], "isp_ids": [], "percent": 0~1, "upgrade_paths": [{rule}, {}]}
        rule: {"core_version": [v1, v2], "target_version": upgrade_version}
    返回体:
        {"result": "OK"}  # 表示该升级策略配置成功

"""

# -------------------------------------------------------------------------------------------------------------


@given('prepare an empty upgrade_rule request')
def create_request_body(context):
    context.upgrade_rule = []


@given('prepare a rule_group without rules')
def create_rule_group(context):
    if context.text:
        context.rule_group = eval(context.text)
    else:
        context.rule_group = {
            "user_ids": [],
            "province_ids": [],
            "isp_ids": [],
            "percent": 1,
            "upgrade_paths": []
        }


@given('prepare a rule')
def create_rule(context):
    if context.text:
        context.rule = eval(context.text)
    else:
        context.rule = {
            "core_version": ["0.0.0", "9.9.9"],
            "target_version": TARGET_VERSION
        }


@given('add the rule to rule_group')
def add_rule_to_rule_group(context):
    context.rule_group["upgrade_paths"].append(deepcopy(context.rule))


@given('prepare a rule_group with a rule valid for all versions')
def create_rule_group(context):
    if context.text:
        context.rule_group = eval(context.text)
    else:
        context.rule_group = {
            "user_ids": [],
            "province_ids": [],
            "isp_ids": [],
            "percent": 1,
            "upgrade_paths": []
        }

    context.execute_steps(u"""
        Given prepare a rule
        And add the rule to rule_group
    """)


@given('add the rule_group to upgrade_rule')
def add_rule_group_to_request(context):
    context.upgrade_rule.append(deepcopy(context.rule_group))

# -------------------------------------------------------------------------------------------------------------


@when('upgrade_controller receive the upgrade_rule request')
def send_request(context):

    uri = "/upgrade_rule"
    body_data = context.upgrade_rule

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


@then('upgrade_rule response should be "{response_data}"')
def verify_that_response_data_is_correct(context, response_data):
    actual_result = context.response.json()
    assert_that(actual_result, equal_to(eval(response_data)), "unexpected response")

# -------------------------------------------------------------------------------------------------------------


