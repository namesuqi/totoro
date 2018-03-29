# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from hamcrest import *
from libs.database.mysql_db import MysqlDB
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.dir.const import *

import binascii

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/devs/vod/ctrl-plane/dir#1
    接口说明: vod-channel向dir发送启播请求
    请求参数说明:
        user: 用户名
        url: 视频资源的网络地址
        type: 文件类型，CDN/M3U8/OSS，现在点播统一用CDN
    返回体:
        // 正常返回
        {
            "file_id": string,    // 点播系统中文件的唯一标示id，由自动注册流程生成
            "fsize": long,        // 文件大小，单位Byte
            "url": string,        // 历史遗留字段，忽略
            "psize": int,         // 默认值864，待更新
            "ppc": int,           // 默认值304，待更新
            "cppc": int,          // 默认值12，待更新
            "authTrimedUrl", string,     //可选，有鉴权配置时，鉴权规则删减后的url
            "src": {              // 历史遗留字段，忽略
                "url": string,
                "ext": {...}      // 可选，m3u8文件相关内容，忽略
            }
        }
        // 异常返回
        {
            "error": string,    // error错误码列举如下
            "err_info": string  // 可选，具体描述信息
        }

"""

# -------------------------------------------------------------------------------------------------------------


@given("prepare valid request body of dir_start_channel")
def request_body_of_dir_start_channel(context):
    context.dir_start_channel = {
        "user": USER_CLOUTROPY,
        "url": URL_EXIST,
        "type": TYPE_CDN,
    }


@given("make sure that url '{value}' is in table_files in MySQL")
def add_url_to_mysql(context, value):
    db = MysqlDB()

    sql = "delete from {table} where source = '{url}'".format(table=TABLE_FILES, url=value)
    db.execute(sql)

    file_id = binascii.a2b_hex(context.file_id)
    sql = "insert into {table} (sid, relative_url, file_id, fsize, state, is_public, active_prefix_id, source) " \
          "values ({source_id}, '/auto/test', '{file_id}', 1234567, 2, 1, {domain_id}, '{url}');"\
        .format(table=TABLE_FILES, source_id=SOURCE_ID, file_id=file_id, domain_id=DOMAIN_ID, url=value)
    db.execute(sql)


@given("make sure that url '{value}' is not in table_files in MySQL")
def delete_url_from_mysql(context, value):
    db = MysqlDB()
    sql = "delete from {table} where source = '{url}'".format(table=TABLE_FILES, url=value)
    db.execute(sql)


@given("make sure that user '{value}' is not in table_users in MySQL")
def delete_user_from_mysql(context, value):
    db = MysqlDB()
    sql = "delete from {table} where name = '{username}'".format(table=TABLE_USERS, username=value)
    db.execute(sql)

# -------------------------------------------------------------------------------------------------------------


@when("dir receive dir_start_channel request")
def send_dir_start_channel(context):

    uri = "/start/channel?{0}".format("&".join(["{0}={1}".format(k, v) for k, v in context.dir_start_channel.items()]))

    context.response = send_http_request(
        GET,
        DIR_HOST,
        DIR_PORT,
        uri,
        HEADERS,
        None,
        {}
    )

# -------------------------------------------------------------------------------------------------------------


@then("response data of dir_start_channel should be consistent with file_info in MySQL")
def verify_data_is_right(context):
    response = context.response.json()
    print "response:", response
    mysql_file_info = get_file_info(url=context.dir_start_channel["url"])[0]
    # currently only take care of file_id and fsize
    assert_that(response.get("file_id", None), equal_to(mysql_file_info["file_id"]))
    assert_that(response.get("fsize", None), equal_to(mysql_file_info["fsize"]))


@then("dir should add the file_info to table_files in MySQL")
def verify_auto_register_success(context):
    request_url = context.dir_start_channel["url"]
    mysql_results = get_file_info(url=request_url)
    assert_that(len(mysql_results), equal_to(1),
                "there is {count} '{url}' in MySQL".format(count=len(mysql_results), url=request_url))
    mysql_file_info = mysql_results[0]

    assert_that(mysql_file_info["active_prefix_id"], equal_to(DOMAIN_ID))
    assert_that(mysql_file_info["sid"], equal_to(SOURCE_ID))


@then("response error_type of dir_start_channel should be {error_type}, sometimes {error_type_2}")
def verify_error_type_is_right(context, error_type, error_type_2):
    print "response data:", context.response.json()
    try:
        if error_type in ("None", "null"):
            error_type = None
        assert_that(context.response.json().get("error", None), equal_to(error_type))
    except AssertionError:
        if error_type_2 in ("None", "null"):
            error_type_2 = None
        assert_that(context.response.json().get("error", None), equal_to(error_type_2))


@then("dir should not add the file_info to table_files in MySQL")
def verify_url_not_in_mysql(context):
    request_url = context.dir_start_channel["url"]
    mysql_results = get_file_info(url=request_url)
    assert_that(mysql_results, equal_to([]))

# -------------------------------------------------------------------------------------------------------------


def get_file_info(url=None, file_id=None):
    # get url and file_id from MySQL file_info table
    db = MysqlDB()
    sql = "select sid, relative_url, hex(file_id) as file_id, fsize, psize, ppc, active_prefix_id, source " \
          "from {table} ".format(table=TABLE_FILES)

    if url is not None:
        sql += "where source = '{url}'".format(url=url)
    elif file_id is not None:
        sql += "where hex(file_id) = '{file_id}'".format(file_id=file_id)

    results = db.execute(sql).to_dict()
    print "file_info in MySQL:", results
    return results  # [{}, {}]


# -------------------------------------------------------------------------------------------------------------



