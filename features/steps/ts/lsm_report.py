# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.ts.const import *

import copy

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/devs/vod/ctrl-plane/report#1-lsm-report
    接口说明: SDK向report-srv上传本地的缓存情况
    请求参数说明:
        peer_id: 设备唯一标识符, 128位UUID
        lsmTotal: 缓存总大小
        lsmFree: 缓存可用大小
        diskTotal: 磁盘总大小
        diskFree: 磁盘可用大小
        universe: 是否全量报
        files: 本地缓存的各文件的信息
            file_id: 文件唯一标识符, 128位UUID
            cppc:
            ppc:
            psize: piece size
            fsize: file size
            percent: 文件下载进度
            stat: 文件状态, "downloading", "done", "waiting", "interrupt", "deleted"

"""

# -------------------------------------------------------------------------------------------------------------


@given('prepare valid request body of lsm_report with empty files')
def create_request_body(context):
    context.lsm_report = {
        "diskTotal": DISK_1G,
        "diskFree": DISK_1G,
        "lsmTotal": LSM_200M,
        "lsmFree": LSM_200M,
        "universe": UNIVERSE_TRUE,
        "files": [],
    }


@given('prepare a valid file_info of lsm_report')
def create_file_info(context):
    context.file_info = {
        "file_id": context.file_id,
        "cppc": CPPC,
        "ppc": PPC,
        "psize": PSIZE,
        "fsize": FSIZE_1G,
        "percent": PERCENT_0,
        "stat": STAT_DOWNLOADING,
    }

# -------------------------------------------------------------------------------------------------------------


@given('add file_info to lsm_report')
def add_file_info_to_lsm_report(context):
    context.lsm_report["files"].append(copy.deepcopy(context.file_info))


@given('add {count} file_info to lsm_report')
def add_many_file_info(context, count):
    for i in range(int(count)):
        context.file_info["file_id"] = "F" * 16 + str(i + 1).zfill(16)
        context.lsm_report["files"].append(copy.deepcopy(context.file_info))

# -------------------------------------------------------------------------------------------------------------


@when('report-srv receive the lsm_report request')
def send_request(context):

    url = "/distribute/peers/{0}".format(context.peer_id)
    body_data = context.lsm_report

    context.response = send_http_request(
        POST,
        TS_HOST,
        TS_PORT,
        url,
        HEADERS,
        None,
        body_data
    )

# -------------------------------------------------------------------------------------------------------------


