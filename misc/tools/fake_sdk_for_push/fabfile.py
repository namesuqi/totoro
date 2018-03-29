# coding=utf-8
# Author=JKZ
# 远程部署脚本工具，收集日志（有待更新）
import glob
import time
from fabric.api import *
from fabric.colors import green
from fabric.decorators import roles
from fabric.tasks import execute
from libs.common.tar_file import untar

env.roledefs = {
    'online_test': ['172.30.0.33'],
    "local_debug": ['192.168.1.173'],
    "perf_test": ['172.30.0.23', "172.30.0.29", "172.30.0.30", "172.30.0.27",  # "172.30.0.28"
    ]  # httpdns, mongo1 mongo2, etcd
}

env.user = 'admin'
env.password = 'Yzhxc9!'
remote_dir = "/home/admin/JKZ"


@roles('all')
def task1(nnn):
    print green(nnn)
    run('ls /root/')


@roles('perf_test')
def deploy_fake_sdk():
    run("rm -rf {0}".format(remote_dir))
    run("mkdir {0}".format(remote_dir))
    put("fake_sdk.py", "{0}/fake_sdk.py".format(remote_dir))
    put("conf.py", "{0}/conf.py".format(remote_dir))
    put("start.sh", "{0}/start.sh".format(remote_dir))
    run('chmod +x {0}/start.sh && sed -i "s/\r//" {0}/start.sh'.format(remote_dir))


@roles('perf_test')
def start_fake_sdk():
    run("{0}/start.sh 32 15 &".format(remote_dir))


@roles('online_test')
def stop_fake_sdk():
    # run("{0}/stop.sh &".format(remote_dir), pty=False)
    run("kill -9 `cat {0}/pids`".format(remote_dir))


@roles('perf_test')
def log_dump():
    with cd(remote_dir):
        ip = run("cat ip")
        tar_time = time.strftime("%Y%m%d%H%M", time.localtime())
        run("mv log/ {0}_{1}".format(ip, tar_time))
        run("tar zcvf {0}_{1}.log.tar.gz {0}_{1}".format(ip, tar_time), pty=False)
        # run("rm -rf {0}_{1}".format(ip, tar_time))
        get("{0}_{1}.log.tar.gz".format(ip, tar_time), "log/{0}_{1}.log.tar.gz".format(ip, tar_time))


if __name__ == "__main__":
    # task1()
    x = "sdfdf"
    # execute(deploy_fake_sdk)
    # execute(start_fake_sdk)
    # execute(log_dump)

    # gz_files = glob.glob("log/172*.tar.gz")
    # folder = "log/201712131010"
    # for f in gz_files:
    #     print f
    #     untar(f, f.split("_")[0])

