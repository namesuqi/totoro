# coding=utf-8
# author=zhangshuwei
# 根据各个IDC机器的配置，启动不同的SDK

import optparse
import time
from fabric.api import *
from misc.tools.idc_deploy.const import *

power_sdk_number = 300
powerful_machines = list()
# powerful_machines.append("59.63.166.73")
powerful_machines.append("60.12.145.12")

normal_sdk_number = 100
normal_machines = list()
# normal_machines.append("61.163.30.198")
# normal_machines.append("60.191.239.152")
# normal_machines.append("61.164.110.152")
# normal_machines.append("122.228.207.106")


powerful_seeds = ["admin@{0}:22".format(machine) for machine in powerful_machines]
normal_seeds = ["admin@{0}:22".format(machine) for machine in normal_machines]

# 操作一致的服务器可以放在一组，同一组的执行同一套操作
env.roledefs = {
    'powerful_seeds': powerful_seeds,
    'normal_seeds': normal_seeds
}


@roles('powerful_seeds', 'normal_seeds')
@parallel
def deploy_sdk():
    try:
        run("killall -9 {0}".format(SDK_FILE), timeout=5)
    except:
        pass

    # delete previous sdk folders
    run("rm -rf {0}".format(IDC_SDK_PATH))

    # create sdk dir and conf dir
    run("mkdir -p {0}".format(IDC_SDK_PATH + "/conf"))

    # copy file to remote sdk dir
    put(LOCAL_SDK_FILE, IDC_SDK_FILE)
    put(LOCAL_LOG_CONF, IDC_LOG_CONF)
    run("cd {0} && chmod +x {1}".format(IDC_SDK_PATH, IDC_SDK_FILE))


@roles('powerful_seeds')
@parallel
def start_sdk_for_powerful_seeds():
    start_sdk(power_sdk_number)


@roles('normal_seeds')
@parallel
def start_sdk_for_normal_seeds():
    start_sdk(normal_sdk_number)


@roles('powerful_seeds')
@parallel
def restart_sdk_for_powerful_seeds():
    restart_sdk(power_sdk_number)


@roles('normal_seeds')
@parallel
def restart_sdk_for_normal_seeds():
    restart_sdk(normal_sdk_number)


def start_sdk(num):
    for i in range(num):
        run("cd {0} && mkdir {1} && cp {2} {1}".format(IDC_SDK_PATH, i, SDK_FILE))
        run("cd {0} && cp -r {1} {0}/{2}".format(IDC_SDK_PATH, "conf", i))
        port = i * SDK_PORT_STEP + SDK_PORT_START
        with cd("{0}/{1}".format(IDC_SDK_PATH, i)):
            run("ulimit -c unlimited")
            run("$(nohup ./{0} -p {1} -u {2} > /dev/null 2>&1 &) && sleep 0.1".format(SDK_FILE, port, SDK_PREFIX))


def restart_sdk(num):
    for i in range(num):
        port = i * SDK_PORT_STEP + SDK_PORT_START
        with cd("{0}/{1}".format(IDC_SDK_PATH, i)):
            run("ulimit -c unlimited")
            run("$(nohup ./{0} -p {1} -u {2} > /dev/null 2>&1 &) && sleep 0.1".format(SDK_FILE, port, SDK_PREFIX))


@roles('powerful_seeds', 'normal_seeds')
def stop_sdk():
    try:
        run("killall -9 {0}".format(SDK_FILE), timeout=5)
    except:
        pass


@roles('seeds')
def create_file():
    # just for test
    run("touch /home/admin/1")

if __name__ == "__main__":
    parser = optparse.OptionParser(
        usage="%prog -a [start|stop|restart]",
        version="1.0"
    )
    parser.add_option("-a", "--action", dest="action", type='string', default="start")
    (options, args) = parser.parse_args()
    action = options.action

    start_time = time.time()
    if action == "start":
        # deploy sdk and files
        execute(deploy_sdk)
        # start sdk for each machine
        execute(start_sdk_for_powerful_seeds)
        execute(start_sdk_for_normal_seeds)
    elif action == "stop":
        execute(stop_sdk)
    elif action == "restart":
        execute(stop_sdk)
        # start sdk for each machine
        execute(restart_sdk_for_powerful_seeds)
        execute(restart_sdk_for_normal_seeds)

    end_time = time.time()
    print("Done, cost {0} seconds.".format(end_time-start_time))
