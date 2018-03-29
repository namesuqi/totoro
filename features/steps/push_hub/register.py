# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from hamcrest import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.push_hub.const import *

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/push-hub-srv_api#4
    接口说明: vod-push向push-hub发送注册请求
    返回体:
        {"ip": vod_push_ip}  # push-hub检测到的push-srv的ip
                             # 当http request header中有x-forwarded-for字段时, ip为该字段的值;
                             # 当没有x-forwarded-for字段时, 为request的socket ip

"""

# -------------------------------------------------------------------------------------------------------------


@given('prepare valid request header of register, x-forwarded-for defaults to {push_ip}')
def defaults_register(context, push_ip):
    if push_ip.upper() == "PUSH_IP":
        push_ip = PUSH_IP
    context.register_header = HEADERS
    context.register_header["x-forwarded-for"] = push_ip

# -------------------------------------------------------------------------------------------------------------


@when('push-hub receive the register request')
def send_register_request(context):

    uri = "/register"
    headers = context.register_header

    context.response = send_http_request(
        GET,
        PUSH_HUB_HOST,
        PUSH_HUB_PORT,
        uri,
        headers,
        None,
        {}
    )

# -------------------------------------------------------------------------------------------------------------


@then("response data of register should be source_ip")
def verify_data_is_source_ip(context):
    print "source_ip:", SOURCE_IP
    assert_that(context.response.json(), equal_to({"ip": SOURCE_IP}))


@then("response data of register should be request_ip")
def verify_data_is_request_ip(context):
    request_ip = context.register_header["x-forwarded-for"]
    print "request_ip:", request_ip
    assert_that(context.response.json(), equal_to({"ip": request_ip}))

# -------------------------------------------------------------------------------------------------------------

