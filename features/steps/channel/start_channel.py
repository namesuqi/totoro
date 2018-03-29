# coding=utf-8
# author: JKZ

from behave import *
from hamcrest import *
from libs.request.header_data import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.channel.const import *


@when('sdk send start channel request')
def send_start_channel_request(context):
    context.response = peer_start_channel(HTTP, CHANNEL_HOST, CHANNEL_PORT, context.user, context.peer_id,
                                          context.file_url)


@given('peer id {belongs} to {user}')
def has_peer_id_with_given_user(context, belongs, user):
    if belongs == "belongs":
        if user == "demo":
            # get user_id from mysql
            # then create peer_id
            context.peer_id = "00000000".ljust(32, 'A')
    elif belongs == "doesn't belongs":
        context.peer_id = "FFFFFFFF".ljust(32, 'A')


@given('play user is {user}')
def create_peer_id_with_user_id(context, user):
    context.user = user


@given('file url {belongs} to {user}')
def has_file_url_with_given_user(context, belongs, user):
    if belongs == "belongs":
        if user == "demo":
            # get file_url form mysql
            context.file_url = DEMO_FILE_URL1
    elif belongs == "doesn't belongs":
        context.file_url = "http://127.0.0.0:80/hls/panda.flv"


# @then('the {field} value of response is {expected_value}')
# def verify_response_special_filed_value(context, field, expected_value):
#     print "hi"
#     print context.peer_id
#     print context.response.json()
#     actual_value = context.response.json().get(field, None)
#     print actual_value
#     assert_that(actual_value, equal_to(expected_value), "response {0} value is {1}".format(field, actual_value))


@then('response should be correct')
def verify_response_special_filed_value(context):
    rsp = context.response.json()
    assert_that(dict(rsp).get("psize"), equal_to(PSIZE))
    assert_that(dict(rsp).get("cppc"), equal_to(CPPC))
    assert_that(dict(rsp).get("ppc"), equal_to(PPC))


def peer_start_channel(protocol, host, port, user, peer_id, file_url):
    """
    file play/download
    :param protocol:
    :param host:
    :param port:
    :param user:
    :param peer_id: device unique id, 128 bit UUID, HEX encoding
    :param file_url:URL，URL encoding. String
    :return:
    """

    url = "/startchannel?user=" + str(user) + "&pid=" + str(peer_id) + "&url=" + str(file_url)

    headers = HeaderData().Content__Type('application/json').Accept('application/json').\
        User__Agent('YunshangSDK/2.4.14').get_res()

    response = send_request(
        protocol,
        GET,
        host,
        port,
        url,
        headers,
        None,
        None
    )

    return response

