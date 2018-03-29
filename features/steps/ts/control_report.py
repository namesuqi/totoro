# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.ts.const import *

from copy import deepcopy

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/devs/vod/ctrl-plane/report#2-control-report
    接口说明: SDK向report-srv上传节点的播放情况和供源情况
    请求参数说明:
        peer_id: 设备唯一标识符, 128位UUID
        duration: 汇报间隔, 单位为秒
        seeds: sdk的供源情况
            file_id: 文件唯一标识符, 128位UUID
            cppc: 缓存piece个数
            download: 此次汇报间隔内下载文件产生的数据量, 单位Byte
            provide: 此次汇报间隔内供源产生的数据量, 单位Byte
        channels: sdk的播放情况
            file_id: 文件唯一标识符, 128位UUID
            type: 文件类型, 支持 "vod", "download", "hls", "live_flv", "live_m3u8", "live_ts", "push", "vhls", "xmtp"
            cdn: cdn流量, 单位Byte
            p2p: p2p流量, 单位Byte
            p2penable: p2p是否开启
            op: channel状态, 支持 "add", "del", "playing"
            err_type: 错误类型, 支持 "","E_DECODE_FAIL"

"""

# -------------------------------------------------------------------------------------------------------------


@given('prepare valid request body of control_report with empty seeds and empty channels')
def create_request_body(context):
    context.control_report = {
        "peer_id": context.peer_id,
        "duration": DURATION,
        "seeds": [],
        "channels": [],
    }


@given('prepare a valid seed_info of control_report')
def create_seed_info(context):
    context.seed_info = {
        "file_id": context.file_id,
        "cppc": CPPC,
        "download": DOWNLOAD_1G,
        "provide": PROVIDE_1G,
    }


@given('prepare a valid channel_info of control_report')
def create_channel_info(context):
    context.channel_info = {
        "file_id": context.file_id,
        "type": TYPE_VOD,
        "cdn": CDN_1G,
        "p2p": P2P_2G,
        "p2penable": P2PENABLE_TRUE,
        "op": OP_DEL,
        "err_type": ERROR_NO
    }

# -------------------------------------------------------------------------------------------------------------


@given('add seed_info to control_report')
def add_seed_info_to_control_report(context):
    context.control_report["seeds"].append(deepcopy(context.seed_info))


@given('add channel_info to control_report')
def add_channel_info_to_control_report(context):
    context.control_report["channels"].append(deepcopy(context.channel_info))


@given('add {count} seed_info to control_report')
def add_many_seed_info(context, count):
    for i in range(int(count)):
        context.seed_info["file_id"] = "F" * 16 + str(i + 1).zfill(16)
        context.control_report["seeds"].append(deepcopy(context.seed_info))


@given('add {count} channel_info to control_report')
def add_many_channel_info(context, count):
    for i in range(int(count)):
        context.channel_info["file_id"] = "F" * 16 + str(i + 1).zfill(16)
        context.control_report["channels"].append(deepcopy(context.channel_info))

# -------------------------------------------------------------------------------------------------------------


@when('report-srv receive the control_report request')
def send_request(context):

    uri = "/sdk/control_report/v1"
    body_data = context.control_report

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




