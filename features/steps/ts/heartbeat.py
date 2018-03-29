# coding=utf-8
# author: guzehao

from behave import *
from hamcrest import *
from libs.request.header_data import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.ts.const import *


@when('sdk send heartbeat report')
def send_heartbeat_report(context):
    context.response = peer_heartbeat(HTTP, TS_HOST, TS_PORT, context.peer_id)


def peer_heartbeat(protocol, host, port, peer_id):
    """
    peer heartbeat，sdk -> ts.cloutropy.com
    :param protocol
    :param host
    :param port
    :param peer_id
    :return:
    """
    url = "/session/peers/" + str(peer_id)

    headers = HeaderData().Content__Type('application/json').ACCEPT('application/json').get_res()

    body_data = {}

    response = send_request(
        protocol,
        GET,
        host,
        port,
        url,
        headers,
        None,
        body_data
    )
    return response
