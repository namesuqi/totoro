# coding=utf-8
# author: TH

from behave import *
from hamcrest import *
from libs.request.header_data import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.channel.const import *


@when('channel-srv receives refreshchannel request {if_with} {file_url}')
def receive_refresh_channel(context, if_with, file_url):
    if if_with is "without":
        url = "/refreshchannel?pid=" + str(context.peer_id)
    else:
        url = "/refreshchannel?pid=" + str(context.peer_id) + "&url=" + str(file_url)
    headers = HeaderData().Content__Type('application/json').Accept('application/json').\
        User__Agent('YunshangSDK/4.2.7').get_res()
    context.response = send_http_request(
        GET,
        CHANNEL_HOST,
        CHANNEL_PORT,
        url,
        headers,
        None,
        None
    )
