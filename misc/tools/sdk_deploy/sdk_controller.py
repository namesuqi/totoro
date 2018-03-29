# coding=utf-8
# author=zhangshuwei

import requests
import json
from libs.common.remoter import *
from misc.tools.sdk_deploy.const import *


def deploy_sdk(ip, user, passwd, sdk_file_name):
    # kill previous processes
    kill_cmd = "killall -9 {0}".format(sdk_file_name)
    remote_execute(ip, user, passwd, kill_cmd)

    # delete previous sdk
    rm_cmd = "rm -rf {0}".format(REMOTE_SDK_PATH)
    remote_execute(ip, user, passwd, rm_cmd)

    # create sdk dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_SDK_PATH)
    remote_execute(ip, user, passwd, mkdir_cmd)

    # create sdk conf dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_SDK_PATH+"/conf")
    remote_execute(ip, user, passwd, mkdir_cmd)

    # copy file to remote sdk dir
    local_sdk = "{0}/{1}".format(LOCAL_SDK_DIR, sdk_file_name)
    copy_file_to(ip, user, passwd, local_sdk, REMOTE_SDK)
    copy_file_to(ip, user, passwd, LOCAL_LOG_CONF, REMOTE_LOG_CONF)

    # make sdk executable
    chmod_cmd = "chmod +x {0}".format(REMOTE_SDK)
    remote_execute(ip, user, passwd, chmod_cmd)


def start_sdk(ip, user, passwd, num, sdk_file_name):
    for i in range(num):
        sdk_folder_name = sdk_file_name[:5] + "-" + str(i)
        mkdir_cmd = "cd {0} && mkdir {1} && cp {2} {1}".format(REMOTE_SDK_PATH, sdk_folder_name, sdk_file_name)
        remote_execute(ip, user, passwd, mkdir_cmd)
        copy_conf_cmd = "cd {0} && cp -r {1} {0}/{2}".format(REMOTE_SDK_PATH, REMOTE_CONF_PATH, sdk_folder_name)
        remote_execute(ip, user, passwd, copy_conf_cmd)
        port = i * SDK_PORT_STEP + SDK_PORT_START

        cmd = "ulimit -c unlimited && cd {0}/{1} && nohup ./{2}".format(REMOTE_SDK_PATH, sdk_folder_name, sdk_file_name)
        start_cmd = "{0} -p {1} -u {2} > /dev/null 2>&1 &".format(cmd, port, SDK_PREFIX)
        remote_execute(ip, user, passwd, start_cmd)


def get_peer_ids_by_conf(ip, user, passwd, num, sdk_file_name):
    peer_ids = list()
    for i in range(num):
        sdk_folder_name = sdk_file_name[:5] + "-" + str(i)
        sdk_path = "{0}/{1}".format(REMOTE_SDK_PATH, sdk_folder_name)
        cmd = "cat {0}/yunshang/yunshang.conf".format(sdk_path)
        line = remote_execute_result(ip, user, passwd, cmd)
        peer_id = json.loads(line).get("peer_id", None)
        print(peer_id)
        peer_ids.append(peer_id)
    return peer_ids


def get_id_by_ajax(ip, num, port=SDK_PORT_START):
    peer_ids = list()
    distance = 0
    for i in range(num):
        url = "http://{0}:{1}{2}".format(ip, port + distance, "/ajax/conf")
        headers = dict()
        headers["accept"] = 'application/json'
        headers["content-type"] = 'application/json'
        res = requests.get(url, headers=headers)
        peer_id = json.loads(res.content).get("peer_id", None)
        print peer_id
        peer_ids.append(peer_id)
        distance += SDK_PORT_STEP

    return peer_ids


def stop_sdk(ip, user, passwd, sdk_file_name):
    kill_cmd = "killall -9 {0}".format(sdk_file_name)
    remote_execute(ip, user, passwd, kill_cmd)


def get_sdk_version(ip, user, passwd, port=SDK_DEFAULT_PORT):
    # try:
    #     url = "http://{0}:{1}{2}".format(ip, str(port), "/ajax/version")
    #     headers = dict()
    #     headers["accept"] = 'application/json'
    #     print url
    #
    #     res = requests.get(url, headers=headers, timeout=10)
    #     return json.loads(res.content).get("core", None)
    # except:
    #     return 0

    cmd = "curl http://{0}:{1}{2}".format(ip, str(port), "/ajax/version")
    result = remote_execute_result(ip, user, passwd, cmd)
    return json.loads(result).get("core", None)


if __name__ == "__main__":
    pass
    # ip = REMOTE_IP
    # user = ROOT_USER
    # passwd = ROOT_PASSWD
    # num = 5
    # sdk_file_name = SDK_DEFAULT_FILE
    # deploy_sdk(ip, user, passwd, sdk_file_name)
    # start_sdk(ip, user, passwd, num, sdk_file_name)
    # get_peer_ids_by_conf(ip, user, passwd, num, sdk_file_name)
    # get_id_by_ajax(ip, num, port=SDK_PORT_START)
    # stop_sdk(ip, user, passwd, sdk_file_name)
