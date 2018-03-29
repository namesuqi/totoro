# coding=utf-8
# Author=JKZ
from behave import *
from hamcrest import *

from features.steps.stun_hub.distribute_task import get_rrpc_commands
from libs.database.redis_single import redis_single_get_list
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.stun_hub.const import *

import json

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/stun-hub-srv_api#4-p2p
    接口说明: stun-hub接收反向控制禁用指定节点p2p功能的请求, p2p-ops -> stun-hub
    请求参数说明:
        peer_ids: 由peer_id组成的list
    请求体:
        {"peer_ids": [String, ...]}
    返回体:
        {}

"""


# -------------------------------------------------------------------------------------------------------------


@given("prepare valid request body of p2p_disable")
def create_peer_ids(context):
    context.p2p_enable = {"peer_ids": []}
    context.rrpc_tasks = []


# -------------------------------------------------------------------------------------------------------------


@given("add a valid peer_id to p2p_disable")
def add_task_info_to_tasks(context):
    context.p2p_enable["peer_ids"].append(context.peer_id)

    peer_id = context.peer_id
    stun_ip = context.pnic.get(peer_id, "unknown_stun_ip")
    context.rrpc_tasks.append((stun_ip, peer_id))


# -------------------------------------------------------------------------------------------------------------


@when("stun-hub receive the p2p_disable request")
def send_request(context):
    uri = "/p2p_disable"
    body_data = context.p2p_enable

    context.response = send_http_request(
        POST,
        STUN_HUB_HOST,
        STUN_HUB_PORT,
        uri,
        HEADERS,
        None,
        body_data
    )


@then("there should be {count} p2p_disable in RRPC_{stun_ip}")
def verify_rrpc_in_redis(context, count, stun_ip):
    redis_value = get_rrpc_commands(stun_ip)
    assert_that(len(redis_value), equal_to(int(count)))


@then("rrpc_command about p2p_disable in RRPC_{expect_stun_ip} should be correct")
def verify_rrpc_is_correct(context, expect_stun_ip):
    if expect_stun_ip.upper() == "STUN_IP":
        expect_stun_ip = STUN_IP
    expect_rrpc_commands = {"peer_ids": []}

    for stun_ip, peer_id in context.rrpc_tasks:
        if stun_ip == expect_stun_ip:
            if peer_id not in expect_rrpc_commands["peer_ids"]:
                expect_rrpc_commands["peer_ids"].append(peer_id)

    redis_value = redis_single_get_list("RRPC_{0}".format(expect_stun_ip))
    for actual_rrpc_command in redis_value:
        actual_rrpc_command = json.loads(actual_rrpc_command)
        assert_that(actual_rrpc_command["cmd"], equal_to("p2p_disable"), "cmd should be {0}".format("p2p_disable"))
        assert_that(len(actual_rrpc_command["peer_ids"]), equal_to(len(expect_rrpc_commands["peer_ids"])),
                    "peer_ids count must be wrong")
        assert_that(sorted(actual_rrpc_command["peer_ids"]), equal_to(sorted(expect_rrpc_commands["peer_ids"])),
                    "peer_ids should be equal")
