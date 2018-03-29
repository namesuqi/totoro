# coding=utf-8
# __author__ = 'liwenxuan'
#

from behave import *
from hamcrest import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.httpdns.const import *
from libs.database.etcd_handler import *


# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/httpdns-srv_api#2-ip   (点播与直播的接口一致)
    接口说明: sdk向httpdns请求解析指定的域名组
    请求参数说明:
        host: 需要解析的域名组
        ip: 可选, 优先从请求列表中获取ip, 如果没有这个参数, 使用请求连接的源ip
    返回体:
        [
            {
                "host": String,
                "ips": [String, ...],
                "ttl": Number
            },
            ...
        ]

"""

# -------------------------------------------------------------------------------------------------------------


@given('prepare valid request body of get_hosts, group defaults to crazycdn')
def defaults_get_hosts(context):
    context.get_hosts = {
        "groupName": GROUP_CRAZYCDN,
        "ip": PARAM_IP,
        "pid": ""
    }


@given('prepare a url about groupName with {peer_id}')
def set_field(context, peer_id):
    context.peer_id = peer_id
    # 设置请求域名组的url参数：get httpdns.crazycdn.com/httpdns/hosts?groupName=?&pid=?
    context.get_hosts = {
        "groupName": "crazycdn.com",
        "pid": context.peer_id
    }


@given('prepare a url about groupName but with empty peer_id')
def set_field(context):
    context.peer_id = ""
    # 设置请求域名组的url参数：get httpdns.crazycdn.com/httpdns/hosts?groupName=?&pid=?
    context.get_hosts = {
        "groupName": "crazycdn.com",
        "pid": context.peer_id
    }


@given('prepare a url about groupName without peer_id')
def set_url_without_pid(context):
    context.get_hosts = {
        # 设置请求指定域名的url参数：get httpdns.crazycdn.com/httpdns/host?host=?pid=?
        "groupName": "crazycdn.com"
    }
# -------------------------------------------------------------------------------------------------------------


@when("httpdns receive get_hosts request")
def send_get_hosts(context):

    uri = "/httpdns/hosts?{0}".format("&".join(["{0}={1}".format(k, v) for k, v in context.get_hosts.items()]))

    context.response = send_http_request(
        GET,
        HTTPDNS_HOST,
        HTTPDNS_PORT,
        uri,
        HEADERS,
        None,
        {}
    )

# -------------------------------------------------------------------------------------------------------------


@then("response data of get_hosts should be {data}")
def verify_ips_is_right(context, data):
    pass

# -------------------------------------------------------------------------------------------------------------


@given('httpdns user domain info has been configured ok with the {user_id} of {user_name} and {host_ip} of {host}')
def config_httpdns(context, user_name, host, host_ip, user_id):
    context.host = host
    context.user_name = user_name
    context.host_ip = host_ip
    context.user_id = user_id
    # 创建用户对应域名key
    context.user_domain_key = "/business/httpdns/v2/domain_ip_map/" + context.user_name
    # 创建用户key
    context.users_key = "/business/httpdns/v2/users/" + user_id
    user_info = {
        context.user_domain_key: {
            context.host: {"ips": {"default": [context.host_ip]}, "ttl": 1800}
        },
        context.users_key: {
            "ip_group": context.user_name
        }
    }
    # 在ETCD中添加指定域名IP信息
    etcd_set_group(user_info)


@given('httpdns has been just configured ok with the {user_id} of {user_name}')
def configure_httpdns(context, user_id, user_name):
    context.user_name = user_name
    context.user_id = user_id
    # 创建用户对应域名key
    context.user_domain_key = "/business/httpdns/v2/domain_ip_map/" + context.user_name
    # 创建用户key
    context.users_key = "/business/httpdns/v2/users/" + user_id
    user_info = {
        context.user_domain_key: {
        },
        context.users_key: {
            "ip_group": context.user_name
        }
    }
    # 在ETCD中添加指定域名IP信息
    etcd_set_group(user_info)


@given('httpdns user domain info is not configured with the {user_id} of {user_name} and {host}')
def del_user_info(context, user_id, user_name, host):
    context.user_name = user_name
    context.user_id = user_id
    context.host = host
    # 删除用户对应域名key
    context.user_domain_key = "/business/httpdns/v2/domain_ip_map/" + context.user_name
    # 删除用户key
    context.users_key = "/business/httpdns/v2/users/" + user_id
    del_etcd_key(context.user_domain_key)
    del_etcd_key(context.users_key)


@then('response hosts info should be correct')
def check_hosts_info(context):
    # 获取get请求域名组列表信息
    resp_info = context.response.json()
    print("Response info:", context.response.json())
    # 从ETCD获取域名组的default列表信息
    default_info = read_etcd_key("/business/httpdns/v2/domain_ip_map/default")
    print("Default info:", default_info)
    # 取指定域名组default的域名IP列表信息
    default_host_info = default_info.get('/business/httpdns/v2/domain_ip_map/default', None)
    # check ips is expected
    for host_info in resp_info:
        print host_info  # {host, ips, ttl}
        host_name = host_info['host']
        print("HostName: ", host_name)
        print("ContextHost: ", context.host)
        # 当host与为该user配置的域名匹配时，判断该域名返回IP与期望值IP是否一致
        if host_name == context.host:
            expected_ips = list()
            expected_ips.append(context.host_ip)
            # 检查get请求返回的指定host的IP与ETCD添加的IP一致
            assert_that(host_info['ips'], equal_to(expected_ips))
        else:
            # 当host与为该user配置的域名不匹配时，判断域名返回IP与ETCD默认返回IP是否一致
            expected_host_ips = default_host_info.get(host_name, None)
            # 将单个域名IP与get请求返回中该域名IP的值作比较
            assert_that(host_info['ips'], equal_to(expected_host_ips.get('ips').get('default')))


@then('response hosts info should be default')
def check_hosts_info_default(context):
    # 获取get请求域名组列表信息
    resp_info = context.response.json ()
    print("Response info:", context.response.json ())
    # 从ETCD获取域名组的default列表信息
    default_info = read_etcd_key("/business/httpdns/v2/domain_ip_map/default")
    print("Default info:", default_info)
    for host_info in resp_info:
        host_name = host_info['host']
        # 取指定域名组default的域名IP列表信息
        default_host_info = default_info.get('/business/httpdns/v2/domain_ip_map/default', None)
        expected_host_ips = default_host_info.get(host_name, None)
        # 将单个域名IP与get请求返回中该域名IP的值作比较
        assert_that(host_info['ips'], equal_to(expected_host_ips.get('ips').get('default')))