# coding=utf-8
# __author__ = 'liwenxuan'

from behave import *
from hamcrest import *
from libs.database.mysql_db import MysqlDB
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.dir.const import *

from features.steps.dir.dir_start_channel import get_file_info

import binascii

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/devs/vod/ctrl-plane/dir#2-file_id
    接口说明: vod-channel向dir发送获取file_id对应的视频文件相关信息的请求
    请求参数说明:
        file_id: 点播系统中文件的唯一标示id，由自动注册流程生成
    返回体:
        // 正常返回
        {

            "url": string,         //视频文件URL，忽略
            "size": long,          //文件大小，单位Byte
            "sourceType": string,  //数据源类型(M3U8,CDN,OSS...)
            "source_url": string,  //源URL，用于访问视频资源
            "ext": string          //非M3U8时为""，M3U8时形式如"[["url1",size1],["url2",size2],......]"，
        }
        // 异常返回
        {
            "error": string,    // error错误码列举如下
            "err_info": string  // 可选，具体描述信息
        }

"""

# -------------------------------------------------------------------------------------------------------------

# be sure do hex transfer when you handle file_id saved in mysql

# -------------------------------------------------------------------------------------------------------------


@given("prepare valid request body of get_file_source")
def request_body_of_get_file_source(context):
    context.get_file_source = {
        "file_id": context.file_id,
    }


@given("make sure that the file_id is in table_files in MySQL")
def add_file_id_to_mysql(context):
    db = MysqlDB()

    file_id = binascii.a2b_hex(context.file_id)
    sql = "delete from {table} where file_id = '{file_id}'".format(table=TABLE_FILES, file_id=file_id)
    db.execute(sql)

    context.url = "http://yunshang.auto.test/auto/test"
    sql = "insert into {table} (sid, relative_url, file_id, fsize, state, is_public, active_prefix_id, source) " \
          "values ({source_id}, '/auto/test', '{file_id}', 1234567, 2, 1, {domain_id}, '{url}');"\
        .format(table=TABLE_FILES, source_id=SOURCE_ID, file_id=file_id, domain_id=DOMAIN_ID, url=context.url)
    db.execute(sql)


@given("make sure that the file_id is not in table_files in MySQL")
def delete_file_id_from_mysql(context):
    db = MysqlDB()
    sql = "delete from {table} where hex(file_id) = '{file_id}'".format(table=TABLE_FILES, file_id=context.file_id)
    db.execute(sql)

# -------------------------------------------------------------------------------------------------------------


@when("dir receive get_file_source request")
def send_get_file_source(context):

    uri = "/user/files/source?{0}".format("&".join(["{0}={1}".format(k, v) for k, v in context.get_file_source.items()]))

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


@then("response data of get_file_source should be consistent with file_info in MySQL")
def verify_data_is_right(context):
    response = context.response.json()
    print "response:", response
    request_file_id = context.get_file_source["file_id"]
    mysql_file_info = get_file_info(file_id=request_file_id)
    assert_that(len(mysql_file_info), equal_to(1),
                "there is {count} {file_id} in MySQL".format(count=len(mysql_file_info), file_id=request_file_id))
    mysql_file_info = mysql_file_info[0]
    # currently only focus on source_url, sourceType and size
    assert_that(response.get("source_url", None), equal_to(mysql_file_info["source"]))
    assert_that(response.get("size", None), equal_to(mysql_file_info["fsize"]))
    assert_that(response.get("sourceType", None), equal_to(TYPE_CDN))

# -------------------------------------------------------------------------------------------------------------



