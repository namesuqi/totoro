# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from hamcrest import *
from libs.request.http_request import *
from libs.request.http_method import *
from libs.database.redis_cluster import *
from features.steps.ts.const import *

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/devs/vod/ctrl-plane/seeds#1-1-get-seeds-request
    接口说明: SDK向seeds-srv发送获取seeds信息的请求
    请求参数说明:
        peer_id: 设备唯一标识符, 128位UUID
        file_id: 文件唯一标识符, 128位UUID
    返回体:
        [{seed_info}, {seed_info}]

"""

# -------------------------------------------------------------------------------------------------------------


def defaults_of_seed_info():
    return {
        # "peer_id"
        "version": VERSION,
        "nat_type": NAT_TYPE,
        "public_ip": PUBLIC_IP,
        "public_port": PUBLIC_PORT,
        "private_ip": PRIVATE_IP,
        "private_port": PRIVATE_PORT,
        "stun_ip": STUN_IP,
        "cppc": CPPC,
        "ppc": PPC,
    }

# -------------------------------------------------------------------------------------------------------------


@given('prepare valid request body of get_seeds')
def get_seeds_defaults(context):
    context.get_seeds = {
        "pid": context.peer_id,
        "fid": context.file_id
    }

# -------------------------------------------------------------------------------------------------------------


@when('seeds-srv receive the get_seeds request')
def send_get_seeds(context):

    uri = "/getseeds?{0}".format("&".join(["{0}={1}".format(k, v) for k, v in context.get_seeds.items()]))

    context.response = send_http_request(
        GET,
        TS_HOST,
        TS_PORT,
        uri,
        HEADERS,
        None,
        {}
    )

# -------------------------------------------------------------------------------------------------------------


@then('seeds-srv should return seeds in FOSC correctly')
def verify_get_seeds_data(context):
    seeds_list = context.response.json().get('seeds')
    assert_that(seeds_list, equal_to([]))


@then('seeds-srv should return at most {count} seeds')
def verify_get_seeds_length(context, count):
    seeds_list = context.response.json().get('seeds')
    assert 0 < len(seeds_list) <= count

# -------------------------------------------------------------------------------------------------------------


# FOSC之后将由策略处理, 且FOSC的格式尚未定论, 暂不关注FOSC相关的步骤及用例
# @given('add {count} seeds to the FOSC in redis')
# def add_seeds_to_redis(context, count):
#     for i in range(int(count)):
#         peer_id = "FFFFFFFF" + str(i + 1).zfill(24)
#         redis_cluster_fosc_add(context.file_id, ISP_100017, peer_id, **defaults_of_seed_info())
#
#
# @given('delete the FOSC in redis')
# @then('delete the FOSC in redis')
# def delete_seeds_in_redis(context):
#     redis_key = "{FOSC_{0}_{1}}".format(context.file_id, ISP_100017)
#     redis_cluster_delete_key(redis_key)
#
#
# @then('seeds_info is not saved to redis cluster')
# def verify_seeds_info_not_in_redis_cluster(context):
#     redis_key = "FOSC_{0}_{1}".format(context.get_seeds.get("fid", ""), ISP_100017)
#     redis_seeds_info = redis_cluster_string_get(redis_key).get("value", None)
#     assert_that(None, equal_to(redis_seeds_info))

# -------------------------------------------------------------------------------------------------------------






