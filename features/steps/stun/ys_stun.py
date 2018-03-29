# coding=utf-8
# author: zengyuetian

from behave import *
from hamcrest import *
from libs.udp_request.stun_udp_req import *
from libs.udp_response.stun_udp_resp import *
from features.steps.stun.const import *
from features.steps.parse_number import *


@Given("stun is ready")
def stun_is_ready(context):
    pass


@when(u'peer send step {step} to stun port {port}')
def peer_send_step_to_stun_port(context, step, port):
    context.udp_resp = sdk_query_type_req(STUN_HOST, port, step, listening_port=60000, udp_check=True)


@when(u'peer send short step to stun port {port:Number}')
def peer_send_short_step_to_stun_port(context, port):
    context.udp_resp = sdk_query_type_req_indefinite(STUN_HOST, port, "", listening_port=60000, udp_check=True)


@then(u'response step is {step1:Number} or {step3:Number}')
def response_step_is_or(context, step1, step3):
    context.resps = parse_stun_rsp_data(context.udp_resp)
    step = context.resps[0]
    print("step is {0}".format(step))
    if step == step1 or step == step3:
        assert True
    else:
        assert False, "step should be {0} or {1}".format(step1, step3)


@then(u'response port is {port:Number}')
def step_impl(context, port):
    resp_port = context.resps[1]
    print("real port is {0}".format(resp_port))
    if resp_port != port:
        assert False, "resp port should be {0}".format(port)


@then(u'response is None')
def response_is_none(context):
    resp = parse_stun_rsp_data(context.udp_resp)
    print("resp is {0}".format(resp))
    assert resp is None, "resp should be None"



