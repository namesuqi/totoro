# coding=utf-8
# author=zhangshuwei
# remote control machines
import json
from fabric.api import *
from misc.tools.sdk_deploy.const import *

# 操作一致的服务器可以放在一组，同一组的执行同一套操作
env.roledefs = {
            'seed_machines': ['root@192.168.4.237:22', 'root@192.168.4.236:22'],
            'test_server': ['root@192.168.4.236:22', ]
            }

env.password = 'root'  # 若各机器密码不一致，则打通所有ssh就行了

sdk_file_name = SDK_DEFAULT_FILE  # eg. "ys_service_static", "debug_ys_service_static"
num = SDK_NUM  # sdk num on each machine


@roles('seed_machines')
def deploy_sdk():
    # kill previous processes
    try:
        run("killall -9 {0}".format(sdk_file_name), timeout=5)
    except:
        pass

    # delete previous sdk
    run("rm -rf {0}".format(REMOTE_SDK_PATH))

    # create sdk dir and conf dir
    run("mkdir -p {0}".format(REMOTE_SDK_PATH))
    run("mkdir -p {0}".format(REMOTE_SDK_PATH+"/conf"))

    # copy file to remote sdk dir
    local_sdk = "{0}/{1}".format(LOCAL_SDK_DIR, sdk_file_name)
    put(local_sdk, REMOTE_SDK)
    put(LOCAL_LOG_CONF, REMOTE_LOG_CONF)
    run("cd {0} && chmod +x {1}".format(REMOTE_SDK_PATH, sdk_file_name))


@roles('seed_machines')
def start_sdk():
    for i in range(num):
        sdk_folder_name = sdk_file_name[:5] + "-" + str(i)
        run("cd {0} && mkdir {1} && cp {2} {1}".format(REMOTE_SDK_PATH, sdk_folder_name, sdk_file_name))
        run("cd {0} && cp -r {1} {0}/{2}".format(REMOTE_SDK_PATH, REMOTE_CONF_PATH, sdk_folder_name))
        port = i * SDK_PORT_STEP + SDK_PORT_START
        with cd("{0}/{1}".format(REMOTE_SDK_PATH, sdk_folder_name)):
            run("ulimit -c unlimited")
            run("$(nohup ./{0} -p {1} -u {2} > /dev/null 2>&1 &) && sleep 1".format(sdk_file_name, port, SDK_PREFIX))
            # sleep 1s to avoid connection closed too early


@roles('seed_machines')
def stop_sdk():
    run("killall -9 {0}".format(sdk_file_name))


@roles('seed_machines')
def get_peer_ids_by_conf():
    peer_ids = list()
    for i in range(num):
        sdk_folder_name = sdk_file_name[:5] + "-" + str(i)
        sdk_path = "{0}/{1}".format(REMOTE_SDK_PATH, sdk_folder_name)
        line = run("cat {0}/yunshang/yunshang.conf".format(sdk_path))
        peer_id = json.loads(line).get("peer_id", None)
        peer_ids.append(peer_id)
    return peer_ids


@roles('seed_machines')
def get_id_by_ajax():
    peer_ids = list()
    distance = 0
    for i in range(num):
        cmd = "curl http://127.0.0.1:{0}{1}".format(SDK_PORT_START + distance, "/ajax/conf")
        res = run(cmd)
        peer_id = json.loads(res).get("peer_id", None)
        print peer_id
        peer_ids.append(peer_id)
        distance += SDK_PORT_STEP

    return peer_ids


@roles('test_server')
def test_task():
    # just test
    with cd("/root/"):
        run("ls -l /root/")
        test_hosts = run("cat /etc/hosts")
        print test_hosts


def do_test():
    # execute(task1)
    execute(test_task)


def sdk_start():
    execute(deploy_sdk)
    execute(start_sdk)
    # execute(stop_sdk)
    # execute(get_peer_ids_by_conf)


if __name__ == "__main__":
    execute(test_task)
    # do_test()
    # print execute(get_peer_ids_by_conf)
    # execute(stop_sdk)
