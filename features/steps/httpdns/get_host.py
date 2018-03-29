# coding=utf-8
# __author__ = 'liwenxuan'


from behave import *
from hamcrest import *

from libs.database.etcd_handler import *
from libs.request.http_request import *
from libs.request.http_method import *
from features.steps.httpdns.const import *
import json

# -------------------------------------------------------------------------------------------------------------

"""

    接口文档: http://10.3.0.10/root/doc/wikis/httpdns-srv_api#1-ip   (点播与直播的接口一致)
    接口说明: sdk向httpdns请求解析指定的域名
    请求参数说明:
        host: 需要解析的域名, 只能有一个域名
        ip: 可选, 优先从请求列表中获取ip, 如果没有这个参数, 使用请求连接的源ip
    返回体:
        {
            "host": String,
            "ips": [String, ...],
            "ttl": Number
        }

"""

# -------------------------------------------------------------------------------------------------------------


@given('prepare valid request body of get_host, host defaults to ts')
def defaults_get_host(context):
    context.get_host = {
        "host": HOST_TS,
        "ip": PARAM_IP,
        "pid": ""
    }


@given('prepare a url with {peer_id} and {host}')
def set_field(context, peer_id, host):
    context.host = host
    context.peer_id = peer_id
    print "CONTEXT.HOST:", context.host
    context.get_host = {
        # 设置请求指定域名的url参数：get httpdns.crazycdn.com/httpdns/host?host=?pid=?
        "host": context.host,
        "pid": context.peer_id
    }


@given('prepare a url with empty peer_id but with {host}')
def set_field(context, host):
    context.host = host
    context.peer_id = ""
    print "CONTEXT.HOST:", context.host
    context.get_host = {
        # 设置请求指定域名的url参数：get httpdns.crazycdn.com/httpdns/host?host=?pid=?
        "host": context.host,
        "pid": context.peer_id
    }


@given('prepare a url without peer_id but with {host}')
def set_url_without_pid(context, host):
    context.host = host
    context.get_host = {
        # 设置请求指定域名的url参数：get httpdns.crazycdn.com/httpdns/host?host=?pid=?
        "host": context.host
    }

# -------------------------------------------------------------------------------------------------------------


@when("httpdns receive get_host request")
def send_get_host(context):

    uri = "/httpdns/host?{0}".format("&".join(["{0}={1}".format(k, v) for k, v in context.get_host.items()]))

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


@then("response data of get_host should be {data}")
def verify_ips_is_right(context, data):
    pass

# -------------------------------------------------------------------------------------------------------------

# def ip_into_int(ip):
#     """
#     将IP转化为整数
#     :param ip:
#     :return:
#     """
#     ip_int = reduce(lambda x, y: (x << 8)+y, map(int, ip.split('.')))
#     return int(ip_int)
#
#
# def httpdns_get_host(protocol, host, port, param_host, src_ip=None, ip_para=False, ip_header=True):
#     """
#     请求指定域名对应的IP
#     :param protocol:
#     :param host:
#     :param port:
#     :param param_host:
#     :param src_ip:
#     :param ip_para: URI中是否携带IP参数
#     :param ip_header: 请求header中是否携带X-Real-IP（负载均衡转发时header所带源IP）
#     :return:
#     """
#     url = "/httpdns/host?host=" + str(param_host)
#     headers = HeaderData().Content__Type('application/json').ACCEPT('application/json').get_res()
#
#     if src_ip is not None and ip_para:
#         url = "/httpdns/host?host=" + str(param_host) + "&ip=" + str(src_ip)
#
#     if src_ip is not None and ip_header:
#         headers = HeaderData().Content__Type('application/json').X__Real__IP(src_ip)\
#             .ACCEPT('application/json').get_res()
#
#     response = send_request(
#         # '[HttpdnsGetHost]',
#         protocol,
#         GET,
#         host,
#         port,
#         url,
#         headers,
#         None,
#         None
#     )
#     return response
#
#
# def httpdns_get_hosts(protocol, host, port, param_group, src_ip=None, ip_para=False, ip_header=True):
#     """
#     请求指定域名组对应的IP
#     :param protocol:
#     :param host:
#     :param port:
#     :param param_group:
#     :param src_ip:
#     :param ip_para: URI中是否携带IP参数
#     :param ip_header: 请求header中是否携带X-Real-IP（负载均衡转发时header所带源IP）
#     :return:
#     """
#
#     url = "/httpdns/hosts?groupName=" + str(param_group)
#     headers = HeaderData().Content__Type('application/json').ACCEPT('application/json').get_res()
#
#     if src_ip is not None and ip_para:
#         url = "/httpdns/hosts?groupName=" + str(param_group) + "&ip=" + str(src_ip)
#
#     if src_ip is not None and ip_header:
#         headers = HeaderData().Content__Type('application/json').X__Real__IP(src_ip)\
#             .ACCEPT('application/json').get_res()
#
#     response = send_request(
#         '[HttpdnsGetHost]',
#         protocol,
#         GET,
#         host,
#         port,
#         url,
#         headers,
#         None,
#         None
#     )
#     return response
#
#
# def check_httpdns_host_res(httpdns_host, httpdns_port, provinces, domains, expect_ip, ips_len, expect_ttl=None,
#                            only=False):
#     """
#     检查httpdns-srv能否根据源IP返回对应域名信息
#     :param provinces: province list
#     :param domains: domain list
#     :param expect_ip: 期望返回的IP的开头两段地址（与配置相对应）, eg:"1.1"
#     :param ips_len: Etcd配置中域名对应IP列表元素个数
#     :param expect_ttl: 期望返回的TTL值, 为None则不检查
#     :param only: 少量请求
#     :return:
#     """
#
#     for k, v in PROVINCE_IP_LIST.iteritems():
#         if k in provinces:
#             if only and hashlib.md5(k).hexdigest()[-1] > '4':
#                 pass
#             else:
#                 print "PROVINCE ID:", k
#                 for ip in v:
#                     print "|||=========================Src ip: %s =========================|||" % str(ip)
#                     ips_index = ip_into_int(ip) % int(ips_len)  # 请求源IP映射到域名IP列表中对应元素索引
#                     for domain in domains:
#                         for i in range(2):
#                             if i == 0:
#                                 # 请求header中携带X-Real-IP参数，URI中不携带IP参数
#                                 res = httpdns_get_host(HTTP, httpdns_host, httpdns_port, domain, ip, ip_para=False,
#                                                        ip_header=True).json()
#                             elif i == 1:
#                                 # 请求URI中携带IP参数，header中不携带
#                                 res = httpdns_get_host(HTTP, httpdns_host, httpdns_port, domain, ip, ip_para=True,
#                                                        ip_header=False).json()
#
#                             time.sleep(0.005)
#                             domain_ips = res["ips"]
#                             if len(domain_ips) != 1:  # 返回域名IP列表中应只有一个IP（需求设计）
#                                 print "Should be only one".ljust(120, "*")
#                                 print "Real domain ips:", domain_ips
#                                 return False
#                             domain_ip = domain_ips[0]
#                             domain_ip_split = domain_ip.split(".")
#                             if domain_ip_split[:2] != expect_ip.split("."):  # 比较域名IP前两段是否与特征值相符
#                                 print "Domain IP should start with %s" % (str(expect_ip)).ljust(120, "*")
#                                 print "Real domain ips:", domain_ips
#                                 return False
#                             if domain_ip_split[-1] != str(ips_index):  # 配置中域名IP最后一段数值表示该IP在列表中的索引
#                                 print "Domain IP should end with %s" % (str(ips_index)).ljust(120, "*")
#                                 print "Real domain ips:", domain_ips
#                                 return False
#                             if expect_ttl is not None:  # 是否检查ttl
#                                 if res["ttl"] != int(expect_ttl):
#                                     print "Domain TTL should be %s" % (str(expect_ttl)).ljust(120, "*")
#                                     print "Real domain ttl:", res["ttl"]
#                                     return False
#     return True
#
#
# def check_httpdns_group_res(httpdns_host, httpdns_port, provinces, domain_group, domains, expect_ip, ips_len,
#                             expect_ttl=None, only=False):
#     """
#     检查httpdns-srv能否根据源IP返回对应域名组信息
#     :param httpdns_host:
#     :param httpdns_port:
#     :param provinces:
#     :param domain_group: 需要获取的域名组，eg: cloutropy.com
#     :param domains: 需要检查的域名列表，不在该列表内的域名不检查，eg: ["ts.cloutropy.com", "report,cloutropy.com"]
#     :param expect_ip:
#     :param ips_len:
#     :param expect_ttl:
#     :param only:
#     :return:
#     """
#     for k, v in PROVINCE_IP_LIST.iteritems():
#         if k in provinces:
#             if only and hashlib.md5(k).hexdigest()[-1] > '4':
#                 pass
#             else:
#                 print "PROVINCE ID:", k
#                 for ip in v:
#                     print "|||=========================Src ip: %s=========================|||" % str(ip)
#                     ips_index = ip_into_int(ip) % int(ips_len)  # 请求源IP映射到域名IP列表中对应元素
#                     for i in range(2):
#                         if i == 0:
#                             res = httpdns_get_hosts(HTTP, httpdns_host, httpdns_port, domain_group, ip, ip_para=False,
#                                                     ip_header=True).json()
#                         elif i == 1:
#                             res = httpdns_get_hosts(HTTP, httpdns_host, httpdns_port, domain_group, ip, ip_para=True,
#                                                     ip_header=False).json()
#                         time.sleep(0.005)
#                         as_len = 0  # 返回域名列表中指定域名元素个数
#                         for domain_info in res:
#                             if domain_info["host"] in domains:  # 返回域名列表中指定域名信息
#                                 as_len += 1
#                                 domain_ips = domain_info["ips"]
#                                 domain_ttl = domain_info["ttl"]
#                                 if len(domain_ips) != 1:
#                                     print "Should be only one".ljust(120, "*")
#                                     print "Should be only one".ljust(120, "*")
#                                     print "Real domain ips:", domain_ips
#                                     return False
#                                 domain_ip = domain_ips[0]
#                                 domain_ip_split = domain_ip.split(".")
#                                 if domain_ip_split[:2] != expect_ip.split("."):
#                                     print "Domain IP should start with %s" % (str(expect_ip)).ljust(120, "*")
#                                     print "Real domain ips:", domain_ips
#                                     return False
#                                 if domain_ip_split[-1] != str(ips_index):
#                                     print "Domain IP should end with %s" % (str(ips_index)).ljust(120, "*")
#                                     print "Real domain ips:", domain_ips
#                                     return False
#                                 if expect_ttl is not None:
#                                     if domain_ttl != int(expect_ttl):
#                                         print "Domain TTL should be %s" % (str(expect_ttl)).ljust(120, "*")
#                                         print "Real domain ttl:", res["ttl"]
#                                         return False
#                         if as_len != len(domains):  # 判断返回中指定域名元素是否有缺失或重复
#                             print "Domain count error.".ljust(120, "*")
#                             print "Actual num: %s, expect num: %s" % (str(as_len), str(len(domains)))
#                             print "Check domains(should exist): %s" % (str(domains))
#                             print "Real domains:",
#                             for x in res: print x["host"], ",",
#                             return False
#
#     return True

# -------------------------------------------------------------------------------------------------------------


@given('httpdns has been configured ok with the {user_id} of {user_name} and {host_ip} of {host}')
def config_httpdns(context, user_name, host, host_ip, user_id):
    context.user_name = user_name
    context.host_ip = host_ip
    context.user_id = user_id
    # 创建用户对应域名key
    context.user_domain_key = "/business/httpdns/v2/domain_ip_map/" + context.user_name
    # 创建用户key
    context.users_key = "/business/httpdns/v2/users/" + user_id
    user_info = {
        context.user_domain_key: {
            host: {"ips": {"default": [context.host_ip]}, "ttl": 1800}
        },
        context.users_key: {
            "ip_group": context.user_name
        }
    }
    # 在ETCD中添加指定域名IP信息
    etcd_set_group(user_info)


@given('httpdns is not configured with the {user_id} of {user_name} and {host}')
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


@then('response host info should be correct')
def check_host_info(context):
    real_value = context.response.json().get("ips", None)
    expect_value = list()
    expect_value.append(context.host_ip)
    # 检查get请求返回的指定host的IP与ETCD添加的IP一致
    assert_that(real_value, equal_to(expect_value))


@then('response host info should be default')
def check_host_info_default(context):
    print("CONTEXT.HOST", context.host)
    real_value = context.response.json().get("ips", None)
    default_info = read_etcd_key("/business/httpdns/v2/domain_ip_map/default")
    default_host_info = default_info.get('/business/httpdns/v2/domain_ip_map/default', None)
    # 从ETCD取出指定host的IP信息
    expected_host_ip = default_host_info.get(context.host, None)
    assert_that(real_value, equal_to(expected_host_ip.get('ips').get('default')))


