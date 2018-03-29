# coding=utf-8
# author: TH

from behave import *
from hamcrest import *
from libs.request.header_data import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.channel.const import *


@when('channel-srv receives starthls request with {channel_type} playlist')
def receive_start_hls(context, channel_type):
    user = ""
    channel_url = ""
    if channel_type == "master":
        channel_url = MASTER_FILE_INFO.get("playlist")
        user = MASTER_FILE_INFO.get("user")
    elif channel_type == "media":
        channel_url = MEDIA_FILE_INFO.get("playlist")
        user = MEDIA_FILE_INFO.get("user")
    elif channel_type == "void":
        print "do nothing"
    url = "/starthls?user=" + str(user) + "&pid=" + str(context.peer_id) + "&url=" + str(channel_url)
    headers = HeaderData().Content__Type('application/json').Accept('application/json').\
        User__Agent('YunshangSDK/5.0.1').get_res()
    context.response = send_http_request(
        GET,
        CHANNEL_HOST,
        CHANNEL_PORT,
        url,
        headers,
        None,
        None
    )


@when('channel-srv receives starthls request with invalid {url_prefix}')
def receive_start_hls(context, url_prefix):
    url = "/starthls?user=demo" + "&pid=" + str(context.peer_id) + \
          "&url=http%3a%2f%2f" + str(url_prefix) + "%2fdemo%2fhls%2focean_4m%2fdemo_ocean_4mbps.m3u8"
    headers = HeaderData().Content__Type('application/json').Accept('application/json'). \
        User__Agent('YunshangSDK/5.0.1').get_res()
    context.response = send_http_request(
        GET,
        CHANNEL_HOST,
        CHANNEL_PORT,
        url,
        headers,
        None,
        None
    )


@then('response of starthls request should be correct')
def check_starthls_response(context):
    response = context.response.json()
    for key in MEDIA_FILE_INFO.keys():
        if key == "playlist" or key == "user":
            print "do nothing"
        else:
            assert_that(response.get(key), equal_to(MEDIA_FILE_INFO.get(key)))
    ext = response.get("src").get("ext")
    segment_data = 0  # 一个segment的大小
    segment_time = 0  # 一个segment需要的时长
    for segment_info in eval(ext):
        segment_data = segment_info[1]+segment_data
        segment_time = segment_info[2]+segment_time
    print segment_data, segment_time
    # 计算平均码率
    avg_bitrate = int(float(segment_data)/float(segment_time)*8)
    # 将计算的平均码率与返回的avg_bitrate匹配
    assert_that(response.get("avg_bitrate"), equal_to(avg_bitrate))
