# coding=utf-8
# author: guzehao

from behave import *
from hamcrest import *
from libs.request.header_data import *
from libs.request.http_request import *
from libs.request.http_method import *
from libs.const.host import *
from libs.database.redis_cluster import *
from features.steps.ts.const import *


@given('peer id is {invalid}')
def invalid_peer_id(context, invalid):
    context.peer_id = invalid


@given("peer id isn't invalid")
def correct_peer_id(context):
    context.peer_id = PEER_ID1


@given('sdk {has} login')
def prepare_database(context, has):
    if has == "has":
        redis_cluster_setex_pnic("600", context.peer_id, VERSION, NAT_TYPE, PUBLIC_IP, PUBLIC_PORT, PRIVATE_IP,
                                 PRIVATE_PORT, PROVINCE_ID_1, ISP_100017, CITY_ID, BEHAVE_HOST)
    elif has == "has not":
        key = "PNIC_"+context.peer_id
        redis_cluster_delete_key(key)


@when('sdk send logout request to ts')
def send_logout_request(context):
    context.response = peer_logout(HTTP, TS_HOST, TS_PORT, context.peer_id)


@then('peer id {be} in database')
def verify_peer_id_in_redis(context, be):
    flag = rc.exists("PNIC_"+context.peer_id)
    if be == 'is':
        assert_that(flag, equal_to(True), "peer id is in database")
    elif be == "isn't":
        assert_that(flag, equal_to(False), "peer id isn't in database")


def peer_logout(protocol, host, port, peer_id):
    """
    peer logout，sdk -> ts.cloutropy.com
    :param protocol:
    :param host:
    :param port:
    :param peer_id
    :return:
    """
    url = "/session/peers/" + str(peer_id)

    headers = HeaderData().Content__Type('application/json').ACCEPT('application/json').get_res()

    body_data = {}

    response = send_request(
        protocol,
        DELETE,
        host,
        port,
        url,
        headers,
        None,
        body_data
    )
    return response
