# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from hamcrest import *

from libs.database.etcd_handler import set_etcd_key
from libs.request.http_request import *
from libs.request.http_method import *
from libs.database.redis_cluster import *
from features.steps.ts.const import *
from libs.data.random_data import random_peer_id

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/devs/vod/ctrl-plane/ts#1-login
    接口说明: SDK向ts-srv发送登录请求
    请求参数说明:
        peer_id: 设备唯一标识符, 128位UUID
        version: sdk的version, 格式为"A.B.C"
        natType: 设备的nat类型, 目前支持 [0, 6]
        publicIP:
        publicPort:
        privateIP:
        privatePort:
        stunIP: 设备连接的stun-srv的ip
        macs: 设备的网卡信息

"""

# -------------------------------------------------------------------------------------------------------------


@given('load defaults of peer_info for hiwifi')
def login_defaults_for_hiwifi(context):
    context.peer_id = random_peer_id(PREFIX_HIWIFI)
    context.peer_ids.append(context.peer_id)

    context.login = {
        "version": VERSION,
        "natType": NAT_TYPE_HIWIFI,
        "publicIP": PUBLIC_IP,
        "publicPort": PUBLIC_PORT,
        "privateIP": PRIVATE_IP,
        "privatePort": PRIVATE_PORT,
        "stunIP": STUN_IP,
        "macs": MACS
    }


@given('valid request body of login')
def login_defaults(context):
    context.login = {
        "version": VERSION,
        "natType": NAT_TYPE,
        "publicIP": PUBLIC_IP,
        "publicPort": PUBLIC_PORT,
        "privateIP": PRIVATE_IP,
        "privatePort": PRIVATE_PORT,
        "stunIP": STUN_IP,
        "macs": MACS
    }


@given('set user {peer_prefix} p2p_enable percent {percent}%')
def set_user_p2p(context, peer_prefix, percent):
    key_name = "/business/ops/sdk/p2p/users/{0}".format(peer_prefix)
    key_value = int(percent)
    set_etcd_key(key_name, key_value)
# -------------------------------------------------------------------------------------------------------------


@when('send login request to ts-server')
def login_send_request(context):

    uri = "/session/peers/{0}".format(context.peer_id)
    body_data = context.login

    context.response = send_http_request(
        POST,
        TS_HOST,
        TS_PORT,
        uri,
        HEADERS,
        None,
        body_data
    )

# -------------------------------------------------------------------------------------------------------------


@given('set macs of login have {count} elements')
def login_set_macs_length(context, count):
    for i in range(int(count)):
        context.login["macs"][str(i)] = "TEST"
    print "login after set_macs_length:", context.login

# -------------------------------------------------------------------------------------------------------------


@then('ts-srv should add the peer_info to PNIC correctly')
def verify_peer_info_in_redis_cluster(context):
    redis_peer_info = get_pnic_value(context.peer_id)

    assert_that(redis_peer_info.get("peer_id"), equal_to(context.peer_id))
    assert_that(redis_peer_info.get("version"), equal_to(context.login.get("version")))
    assert_that(redis_peer_info.get("natType"), equal_to(context.login.get("natType")))
    assert_that(redis_peer_info.get("publicIP"), equal_to(context.login.get("publicIP")))
    assert_that(redis_peer_info.get("publicPort"), equal_to(context.login.get("publicPort")))
    assert_that(redis_peer_info.get("privateIP"), equal_to(context.login.get("privateIP")))
    assert_that(redis_peer_info.get("privatePort"), equal_to(context.login.get("privatePort")))
    assert_that(redis_peer_info.get("stunIP"), equal_to(context.login.get("stunIP")))


@then('ts-srv should add the peer_info for hiwifi to PNIC correctly')
def verify_peer_info_in_redis_cluster(context):
    redis_peer_info = get_pnic_value(context.peer_id)

    if context.login.get("natType") == 3:
        assert_that(redis_peer_info.get("natType"), equal_to(4))
    else:
        assert_that(redis_peer_info.get("natType"), equal_to(context.login.get("natType")))

    assert_that(redis_peer_info.get("peer_id"), equal_to(context.peer_id))
    assert_that(redis_peer_info.get("version"), equal_to(context.login.get("version")))
    assert_that(redis_peer_info.get("publicIP"), equal_to(context.login.get("publicIP")))
    assert_that(redis_peer_info.get("publicPort"), equal_to(context.login.get("publicPort")))
    assert_that(redis_peer_info.get("privateIP"), equal_to(context.login.get("privateIP")))
    assert_that(redis_peer_info.get("privatePort"), equal_to(context.login.get("privatePort")))
    assert_that(redis_peer_info.get("stunIP"), equal_to(context.login.get("stunIP")))


@then('ts-srv should not add the peer_info to PNIC')
def verify_peer_info_not_in_redis_cluster(context):
    assert_that(get_pnic_value(context.peer_id), equal_to(None))

# -------------------------------------------------------------------------------------------------------------


def get_pnic_value(peer_id):
    redis_key = "PNIC_{0}".format(peer_id)
    redis_peer_info = redis_cluster_string_get(redis_key).get("value", None)
    print "peer_info in redis:", redis_peer_info
    return redis_peer_info

# -------------------------------------------------------------------------------------------------------------


