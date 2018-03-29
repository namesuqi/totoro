# coding=utf-8
# author: zengyuetian
"""
Purpose:
--------------------------
deploy code and sdk to remote machine
and then call local_main.py on remote machine
to avoid python paramiko lib ssh connection limitation
to start more than 100 players

Test Scenario:
--------------------------
for multi-nodes stress test
for background traffic test
for multi-channels test

Usage:
--------------------------
cd totoro
python misc/tools/group_vod/main.py <operation> <host.ini>
<operation>:
start:          stop + remove + deploy + start
restart:        stop + start
stop:           stop
replace_sdk:    only replace sdk, don't remove conf/meta/data
sdk:            check how many sdk process is alive
core:           check how many sdk core dump
version:        check sdk version
"""

import inspect
import traceback
import paramiko
import threading
import time
import ConfigParser
import os
import sys
import requests
import json

# flag to support multi-channels
SUPPORT_MULTI_CHANNELS = False

SDK_IP_LIST = []
SDK_NUM_LIST = []
SDK_USER_NAME_LIST = []
SDK_PASSWORD_LIST = []
CHANNEL_URL_LIST = []
LSM_LIST = []
PREFIX_LIST = []

##########################################
# for yunshang IDC, set it to true
# for other IDC or server, set it to false
# keep it to False, do not change it
SCP_COPY = True
##########################################

REQUEST_TIMEOUT = 5  # HTTP request timeout
STREAM_TARGET = 32  # How many stream connection we expected
THREAD_INTERVAL = 30  # Seconds
STOP_THREAD_INTERVAL = 1  # Seconds

# get current dir path
file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
parent_path = os.path.dirname(file_path)

# path definition
REMOTE_SDK_PATH = '/home/admin/vod'
REMOTE_PLAYER_PATH = '/home/admin/vod'
REMOTE_LOG_CONFIG_PATH = '/home/admin/vod/conf'
LOG_CONFIG = "myslog.conf"
SDK_FILE = 'ys_service_static'
INI_FILE = 'host.ini'
REMOTE_SDK_FILE = '{0}/{1}'.format(REMOTE_SDK_PATH, SDK_FILE)

# SDK port definition
SDK_PORT_START = 30000
SDK_PORT_STEP = 10
SSH_PORT = 22

# use and password to access remote machines
USERNAME = "admin"
PASSWORD = ""
ROOT_USERNAME = "root"
ROOT_PASSWORD = "Yunshang2014"

# live channel
CHANNEL_URL = "live_flv/user/xmtv?url=http://panda.test.cloutropy.com/live/livestream.flv"
PURE_URL = "http://pullsdk.test.live.00cdn.com/live/stream999.flv"  # 400Kbps
# PURE_URL = "http://panda.test.cloutropy.com/live/livestream.flv"  # 700Kbps

# Ini configuration file and sdk file need to be placed in current dir
SDK_FILE_PATH = "{0}/{1}".format(parent_path, SDK_FILE)
INI_FILE_PATH = "{0}/{1}".format(parent_path, INI_FILE)

# only get data from SDK which has specified prefix
# 指定使用雷锋前缀的时候，不用加0x
USE_LF_PREFIX = ""
# USE_LF_PREFIX = " -x 00010047 "

# to identify SDK user for boss and ops
# 指定用什么前缀启动的时候，需要加0x
# USER_PREFIX = ""
USER_PREFIX = " -u 0x00010048 "


def read_ini():
    """
    get configure info from ini file
    :return: None
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open(INI_FILE_PATH))
    section_list = config.sections()
    common_config = section_list[0]

    for i in section_list[1:]:
        if config.has_section(i):
            SDK_IP_LIST.append(config.get(i, "IP"))
            # SDK_USER_NAME_LIST.append(config.get(i, "Username"))
            SDK_USER_NAME_LIST.append(USERNAME)
            # SDK_PASSWORD_LIST.append(config.get(i, "Password"))
            SDK_PASSWORD_LIST.append(PASSWORD)
            SDK_NUM_LIST.append(int(config.get(i, "SDK_Number")))
            # CHANNEL_URL_LIST.append(config.get(i, "Channel_URL"))
            CHANNEL_URL_LIST.append(CHANNEL_URL)
            PREFIX_LIST.append(config.get(common_config, "Prefix"))
            LSM_LIST.append(int(config.get(common_config, "Lsm")))
        else:
            break
    print("Machine lists:")
    print SDK_IP_LIST
    print PREFIX_LIST
    print LSM_LIST


class JsonParser(object):
    """
    parse json data field via path
    """

    @staticmethod
    def get_data_by_path(data, path):
        # if start with /，remove /
        if path.startswith("/"):
            path = path[1:]
        key_list = path.split("/")
        num_list = [str(x) for x in range(100)]  # import to support index more than 10

        try:
            for key in key_list:
                if key in num_list:  # for number array
                    index = int(key)
                    data = data[index]
                else:  # for key
                    data = data.get(key)
        except Exception as e:
            data = None

        return data


def send_request(host_ip, host_port, url):
    """
    to get dashboard information
    :param host_ip:
    :param host_port:
    :param url:
    :return:
    """
    url = "http://{0}:{1}{2}".format(host_ip, host_port, url)
    headers = dict()
    headers["accept"] = 'application/json'
    resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    return resp


class RemoteDeployer(object):
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        print [username, password]

    def deploy_folder(self, local_dir, remote_dir, kill_proc=None):
        """
        please make sure killall command is ready on remote machine
        :param local_dir:
        :param remote_dir:
        :param kill_proc:
        :return:
        """
        print "Start Clean for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password, key_filename='/root/.ssh/id_rsa.pub')
        if kill_proc is not None:
            ssh.exec_command("killall -9 {proc}".format(proc=kill_proc))
            print "kill process {proc}".format(proc=kill_proc)
            time.sleep(2)
        command = "rm -rf {dir}".format(dir=remote_dir)
        print command
        ssh.exec_command(command)
        time.sleep(3)
        command = "mkdir -p {dir}".format(dir=remote_dir)
        print command
        ssh.exec_command(command)
        time.sleep(2)
        command = "mkdir -p {dir}".format(dir=REMOTE_LOG_CONFIG_PATH)
        print command
        ssh.exec_command(command)
        time.sleep(2)
        if SCP_COPY:
            self.copy_via_scp(local_dir, remote_dir)
        else:
            self.copy_via_paramiko(local_dir, remote_dir)

        ssh.exec_command("chmod -R 755 {0}".format(remote_dir))
        ssh.close()

    def copy_via_paramiko(self, local_path, remote_path):
        """
        copy files to remote machine via paramiko lib
        :param local_path:
        :param remote_path:
        :return:
        """
        t = paramiko.Transport(self.ip, SSH_PORT)
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print local_path
        print remote_path
        if remote_path == REMOTE_PLAYER_PATH:
            sftp.put(local_path + "/flv_play.py", remote_path + "/flv_play.py")
            sftp.put(local_path + "/flv_parse.py", remote_path + "/flv_parse.py")
            sftp.put(local_path + "/local_main.py", remote_path + "/local_main.py")
            sftp.put(local_path + "/{0}".format(SDK_FILE), remote_path + "/{0}".format(SDK_FILE))
            sftp.put(local_path + "/conf/{0}".format(LOG_CONFIG), remote_path + "/conf/{0}".format(LOG_CONFIG))
        else:
            sftp.put(local_path, remote_path)

        t.close()

    def copy_via_scp(self, local_path, remote_path):
        """
        copy files to remote machine via scp command
        :param local_path:
        :param remote_path:
        :return:
        """
        if SDK_FILE in local_path:
            command = 'scp -r {dir} {user}@{ip}:{path}'.format(
                dir=local_path, user=self.username, ip=self.ip, path=remote_path)
        else:
            command = 'scp -r {dir}/* {user}@{ip}:{path}'.format(
                dir=local_path, user=self.username, ip=self.ip, path=remote_path)
        print "Start Deploy SDK for {ip}".format(ip=self.ip)
        print command
        os.system(command)
        print "End Deploy SDK for {ip}".format(ip=self.ip)


class RemoteNode(object):
    def __init__(self, ip, sdk_nums, url, local_sdk, username, password, lsm, prefix):
        self.local_sdk = local_sdk
        self.sdk_nums = sdk_nums
        self.ip = ip
        self.url = url
        self.username = username
        self.password = password
        self.lsm = lsm
        self.prefix = prefix
        print [username, password]

    def stop_play(self):
        print "Stop play for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        ssh.exec_command("killall -9 python")
        ssh.close()

    def remove_files(self):
        print "remove files for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        ssh.exec_command("rm -rf {dir}".format(dir=REMOTE_SDK_PATH))
        time.sleep(1)
        ssh.exec_command("rm -rf {dir}".format(dir=REMOTE_PLAYER_PATH))
        ssh.close()

    def remove_core_dump(self, path=REMOTE_SDK_PATH):
        print "Remove core dump for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        # remove files
        find_command = "find {path} -name core.* ".format(path=path) + " -exec rm -f {} \;"
        print find_command
        std_in, std_out, std_err = ssh.exec_command(find_command)
        output = std_out.read()
        print output
        ssh.close()

    def remove_data_file(self, path=REMOTE_SDK_PATH):
        print "Remove data file for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        # remove files
        find_command = "find {path} -name yunshang.data ".format(path=path) + " -exec rm -f {} \;"
        print find_command
        std_in, std_out, std_err = ssh.exec_command(find_command)
        output = std_out.read()
        print output
        ssh.close()

    def stop_sdk(self):
        print "Stop sdk for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        ssh.exec_command("killall -9 {sdk}".format(sdk=SDK_FILE))
        ssh.close()

    def stop_live_push(self):
        print "Stop sdk for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, ROOT_USERNAME, ROOT_PASSWORD)
        # STOP LIVE PUSH
        print_str = "{print $2}"
        command = "ps aux | grep {proc} |grep -v grep |awk -F ' ' '{print_str}' | xargs kill -9".format(
            proc="livepush", print_str=print_str)
        print command
        ssh.exec_command(command)
        # STOP PORT SERVER
        command = "ps aux | grep {0} |grep -v grep |awk -F ' ' '{1}' | xargs kill -9".format("portserver", print_str)
        print command
        ssh.exec_command(command)
        ssh.close()

    def start_play(self):
        if SUPPORT_MULTI_CHANNELS:
            start, end = get_url_start_end(self.ip)
        else:
            start = 0
            end = self.sdk_nums

        print "Start play for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)

        command = "cd {player} ; nohup python {player}/local_main.py --num {num} --action start> local_main.log 2>&1 &".format(
            player=REMOTE_PLAYER_PATH, num=self.sdk_nums, url=PURE_URL)
        ssh.exec_command(command)
        print command
        time.sleep(1)
        ssh.close()

    def start_sdk(self):
        print "Start SDK for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        ssh.exec_command("chmod +x {sdk}".format(sdk=REMOTE_SDK_FILE))
        command = "cd {sdk} ; nohup python {sdk}/local_main.py --num {num} --action start --lsm {lsm} --prefix {prefix}> local_main.log 2>&1 &".format(
            sdk=REMOTE_SDK_PATH, num=self.sdk_nums, lsm=self.lsm, prefix=self.prefix)
        ssh.exec_command(command)
        print command
        time.sleep(1)
        ssh.close()

    def restart_sdk(self):
        # restart sdk on remote machines
        print "Start SDK for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        ssh.exec_command("chmod +x {0}".format(REMOTE_SDK_FILE))
        command = "cd {sdk} ; nohup python {sdk}/local_main.py --num {num} --action restart --lsm {lsm} --prefix {prefix}> local_main.log 2>&1 &".format(
            sdk=REMOTE_SDK_PATH, num=self.sdk_nums, lsm=self.lsm, prefix=self.prefix)
        ssh.exec_command(command)
        print command
        time.sleep(1)
        ssh.close()

    def deploy_sdk(self):
        # delete sdk on remote machines
        print "Start Clean for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        ssh.exec_command("killall -9 {0}".format(SDK_FILE))
        time.sleep(1)
        ssh.exec_command("rm -rf {0}/".format(REMOTE_SDK_PATH))
        ssh.exec_command("rm -rf {0}".format(REMOTE_SDK_PATH))
        time.sleep(0.5)
        ssh.exec_command("mkdir -p {0}".format(REMOTE_SDK_PATH))
        time.sleep(0.5)
        ssh.close()

        deployer = RemoteDeployer(self.ip, self.username, self.password)
        if SCP_COPY:
            deployer.copy_via_scp(self.local_sdk, REMOTE_SDK_PATH)
        else:
            deployer.copy_via_paramiko(self.local_sdk, REMOTE_SDK_FILE)

    def done(self):
        print "Stop sdk and stop play for {0}".format(self.ip)
        command = 'sshpass -p {0} ssh -o StrictHostKeyChecking=no {1}@${2} "killall -9 ys_service_static"'.format(
            self.password, self.username, self.ip)
        print command
        os.system(command)

    def deploy_player(self):
        # delete sdk on remote machines
        print "Start deploy player for {0}".format(self.ip)
        deployer = RemoteDeployer(self.ip, self.username, self.password)
        deployer.deploy_folder(parent_path, REMOTE_PLAYER_PATH)

    def find_core_dump(self, path=REMOTE_SDK_PATH):
        # start sdk on remote machines and remove folder
        print "Search core dump for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        # show timestamp for core dump files
        # find_command = "find {0} -name core.* ".format(path) + " -exec ls -l {} \;"
        find_command = "find {0} -name core.* ".format(path)
        # print find_command
        std_in, std_out, std_err = ssh.exec_command(find_command)
        output = std_out.read()
        print output

        print "Host Memory usage: "
        memory_command = "free"
        std_in_mem, std_out_mem, std_err_mem = ssh.exec_command(memory_command)
        print std_out_mem.read()
        ssh.close()
        return len(output.split())

    def check_sdk_version(self, path=REMOTE_SDK_PATH):
        # start sdk on remote machines and remove folder
        command = "curl http://{0}:{1}/ajax/version".format(self.ip, SDK_PORT_START)
        os.system(command)
        print("")

    def find_data_file(self, path=REMOTE_SDK_PATH):
        # start sdk on remote machines and remove folder
        print "Search data file for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        find_command = "find {0} -name yunshang.data ".format(path) + " -exec ls -l {} \;"
        # print find_command
        std_in, std_out, std_err = ssh.exec_command(find_command)
        output = std_out.read()
        print output
        ssh.close()
        return len(output.split())/9

    def find_player(self):
        print "Search player for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        python_command = "ps aux|grep flv_play.py|wc"
        std_in_py, std_out_py, std_err_py = ssh.exec_command(python_command)
        output = std_out_py.read()
        ssh.close()
        result = int(output.split()[0]) - 2
        print "Python player number:{0}".format(result)
        return result

    def replace_sdk(self):
        print "replace sdk for {0}".format(self.ip)

        deployer = RemoteDeployer(self.ip, self.username, self.password)
        if SCP_COPY:
            deployer.copy_via_scp(self.local_sdk, REMOTE_SDK_PATH)
        else:
            deployer.copy_via_paramiko(self.local_sdk, REMOTE_SDK_FILE)

        time.sleep(1)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        command = "cd {sdk}; python replace_sdk.py {num} > replace_sdk.log 2>&1".format(
            sdk=REMOTE_SDK_PATH, num=self.sdk_nums)
        ssh.exec_command(command)
        print command
        time.sleep(1)
        ssh.close()

    def find_sdk(self):
        print "Search sdk for {0}".format(self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, SSH_PORT, self.username, self.password)
        sdk_command = "ps aux|grep {0}|wc".format(SDK_FILE)
        std_in_py, std_out_py, std_err_py = ssh.exec_command(sdk_command)
        output = std_out_py.read()
        ssh.close()
        result = int(output.split()[0]) - 2
        result /= 2  # shell + real
        print "Sdk process number:{0}".format(result)
        return result


def start_play_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH, SDK_USER_NAME_LIST[i],
                      SDK_PASSWORD_LIST[i], LSM_LIST[i], PREFIX_LIST[i])

    node.stop_sdk()
    node.deploy_player()  # deploy player and local_main and sdk
    node.start_play()


def restart_play_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH, SDK_USER_NAME_LIST[i],
                      SDK_PASSWORD_LIST[i], LSM_LIST[i], PREFIX_LIST[i])
    # node.stop_play() vod no player
    node.stop_sdk()  # not deploy player and sdk to save time
    node.start_play()


def start_sdk_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i],LSM_LIST[i], PREFIX_LIST[i])
    node.stop_sdk()
    node.deploy_player()
    node.start_sdk()


def deploy_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH, SDK_USER_NAME_LIST[i],
                      SDK_PASSWORD_LIST[i],LSM_LIST[i], PREFIX_LIST[i])
    node.stop_play()
    node.deploy_player()
    node.stop_sdk()
    # node.deploy_sdk()
    # node.start_sdk()  # create sub folder as 0, 1, 2, ...


def restart_sdk_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i],LSM_LIST[i], PREFIX_LIST[i])
    node.stop_sdk()
    node.restart_sdk()


def stop_play_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i],LSM_LIST[i], PREFIX_LIST[i])
    node.stop_play()
    node.stop_sdk()


def stop_live_push_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i],LSM_LIST[i], PREFIX_LIST[i])
    node.stop_live_push()


def stop_sdk_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i],LSM_LIST[i], PREFIX_LIST[i])
    node.stop_sdk()


def clean_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i], LSM_LIST[i], PREFIX_LIST[i])
    node.remove_files()


def done_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i], LSM_LIST[i], PREFIX_LIST[i])
    node.done()


def replace_sdk_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i],LSM_LIST[i], PREFIX_LIST[i])
    node.replace_sdk()


def remove_core_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i], LSM_LIST[i], PREFIX_LIST[i])
    node.remove_core_dump()


def remove_data_thread(i):
    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i], LSM_LIST[i], PREFIX_LIST[i])
    node.remove_data_file()


class Tester(object):
    """
    test helper class
    """

    @staticmethod
    def start_play_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=start_play_thread, args=(i,))
            t.start()
            time.sleep(THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def start_sdk_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=start_sdk_thread, args=(i,))
            t.start()
            time.sleep(THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def restart_play_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=restart_play_thread, args=(i,))
            t.start()
            time.sleep(THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def deploy_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=deploy_thread, args=(i,))
            t.start()
            time.sleep(THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def restart_sdk_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=restart_sdk_thread, args=(i,))
            t.start()
            print "Thread name is", t.getName()
            time.sleep(THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def stop_play_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=stop_play_thread, args=(i,))
            t.start()
            print "Thread name is", t.getName()
            time.sleep(STOP_THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def stop_live_push_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=stop_live_push_thread, args=(i,))
            t.start()
            print "Thread name is", t.getName()
            time.sleep(10)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def stop_sdk_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=stop_sdk_thread, args=(i,))
            t.start()
            time.sleep(STOP_THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def done_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=done_thread, args=(i,))
            t.start()
            time.sleep(STOP_THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def replace_sdk_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=replace_sdk_thread, args=(i,))
            t.start()
            time.sleep(STOP_THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def clean_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}, {1}".format(i + 1, SDK_IP_LIST[i])
            t = threading.Thread(target=clean_thread, args=(i,))
            t.start()
            time.sleep(STOP_THREAD_INTERVAL)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def core_test():
        while True:
            try:
                core_dump_num = 0
                for i in range(len(SDK_IP_LIST)):
                    print "-----------------------------------------"
                    print "Start for host {0}".format(i + 1)
                    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i], LSM_LIST[i], PREFIX_LIST[i])
                    core_dump_num += node.find_core_dump()
                print "*********************************************"
                print "***** Find {0} core dump files".format(core_dump_num)
                print "*********************************************"
            except:
                pass
            time.sleep(10)

    @staticmethod
    def version_test():
        while True:
            try:
                for i in range(len(SDK_IP_LIST)):
                    print "-----------------------------------------"
                    print "Start for host {0}".format(i + 1)
                    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i], LSM_LIST[i], PREFIX_LIST[i])
                    node.check_sdk_version()
            except:
                pass
            time.sleep(10)

    @staticmethod
    def data_test():
        while True:
            try:
                data_file_num = 0
                for i in range(len(SDK_IP_LIST)):
                    print "-----------------------------------------"
                    print "Start for host {0}".format(i + 1)
                    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i], LSM_LIST[i], PREFIX_LIST[i])
                    data_file_num += node.find_data_file()
                print "*********************************************"
                print "***** Find {0} data files".format(data_file_num)
                print "*********************************************"
            except:
                pass
            time.sleep(10)

    @staticmethod
    def player_test():
        while True:
            try:
                player_num = 0
                for i in range(len(SDK_IP_LIST)):
                    print "-----------------------------------------"
                    print "Start for host {0}".format(i + 1)
                    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i],LSM_LIST[i], PREFIX_LIST[i])
                    player_num += node.find_player()
                print "*********************************************"
                print "***** Find {0} player".format(player_num)
                print "*********************************************"
            except:
                pass
            time.sleep(10)

    @staticmethod
    def sdk_test():
        while True:
            try:
                sdk_num = 0
                print len(SDK_IP_LIST), SDK_IP_LIST
                for i in range(len(SDK_IP_LIST)):
                    print "-----------------------------------------"
                    print "Start for host {0}".format(i + 1)
                    node = RemoteNode(SDK_IP_LIST[i], SDK_NUM_LIST[i], CHANNEL_URL_LIST[i], SDK_FILE_PATH,
                                      SDK_USER_NAME_LIST[i], SDK_PASSWORD_LIST[i], LSM_LIST[i], PREFIX_LIST[i])
                    sdk_num += node.find_sdk()
                print "*********************************************"
                print "***** Find {0} sdk process".format(sdk_num)
                print "*********************************************"
            except:
                pass
            time.sleep(10)

    @staticmethod
    def remove_core_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}".format(i + 1)
            t = threading.Thread(target=remove_core_thread, args=(i,))
            t.start()

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def remove_data_test():
        for i in range(len(SDK_IP_LIST)):
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}".format(i + 1)
            t = threading.Thread(target=remove_data_thread, args=(i,))
            t.start()

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

    @staticmethod
    def print_help():
        print "Please use control type: [start|stop|core|sdk]"


def get_cid_data(host_ip, host_port):
    global cid_dict
    key = "{0}:{1}".format(host_ip, host_port)
    try:
        res = send_request(host_ip, host_port, "/ajax/scheduler")
        reading_cid = JsonParser.get_data_by_path(json.loads(res.content), "/0/reading_cid")

    except Exception as e:
        reading_cid = None
        # print e

    old_cid = cid_dict.get(key, None)
    if key == "106.15.139.28:60610" or key == "106.15.139.28:60600":
        print "{0} new:{1} old:{2}".format(key, reading_cid, old_cid)

    if mutex.acquire(1):
        # if current == old, cid has problem
        if old_cid == reading_cid:
            bad_cid_list.append(key)
        cid_dict[key] = reading_cid  # save current cid
        mutex.release()


def get_sdk_data(host_ip, host_port):
    global cid_dict, sdk_data_list
    try:
        res = send_request(host_ip, host_port, "/ajax/report")
        p2p_percent = json.loads(res.content).get("p2p_percent", None)
        seed_num = json.loads(res.content).get("seed_num", None)
        stream_num = json.loads(res.content).get("stream_num", None)
        download_rate = json.loads(res.content).get("download_rate", None)

        conf = send_request(host_ip, host_port, "/ajax/conf")
        peer_id = json.loads(conf.content).get("peer_id", None)

        if mutex.acquire(1):
            sdk_data_dict = dict()
            sdk_data_dict["id"] = "{0}:{1}".format(host_ip, host_port)
            sdk_data_dict["p2p_percent"] = p2p_percent
            sdk_data_dict["seed_num"] = seed_num
            sdk_data_dict["stream_num"] = stream_num
            sdk_data_dict["download_rate"] = download_rate
            sdk_data_dict["peer_id"] = peer_id
            sdk_data_list.append(sdk_data_dict)

            p2p_list.append(p2p_percent)
            seed_num_list.append(seed_num)
            stream_num_list.append(stream_num)
            download_rate_list.append(download_rate)
            # if stream_num < STREAM_TARGET:
            #     bad_stream_list.append("{0}:{1}".format(host_ip, host_port))

            mutex.release()
    except Exception as e:
        if mutex.acquire(1):
            sdk_data_dict = dict()
            sdk_data_dict["id"] = "{0}:{1}".format(host_ip, host_port)
            sdk_data_dict["p2p_percent"] = 0
            sdk_data_dict["seed_num"] = 0
            sdk_data_dict["stream_num"] = 0
            sdk_data_dict["download_rate"] = 0
            sdk_data_dict["peer_id"] = ""
            sdk_data_list.append(sdk_data_dict)

            p2p_list.append(0)
            seed_num_list.append(0)
            stream_num_list.append(0)
            download_rate_list.append(0)
            # bad_p2p_list.append("{0}:{1}".format(host_ip, host_port))
            # bad_stream_list.append("{0}:{1}".format(host_ip, host_port))
            mutex.release()


def print_bad_sdk():
    global sdk_data_list
    zero_p2p_list = list()
    zero_download_list = list()

    for sdk_data in sdk_data_list:
        if sdk_data["p2p_percent"] == 0:
            zero_p2p_list.append(sdk_data["id"])
        if sdk_data["download_rate"] == 0:
            zero_download_list.append(sdk_data["id"])
    print "SDK with p2p rate 0: ", len(zero_p2p_list)
    print zero_p2p_list
    print "SDK with download rate 0: ", len(zero_download_list)
    print zero_download_list


def print_less_99_sdk():
    global sdk_data_list
    p2p_list = list()
    for sdk_data in sdk_data_list:
        if sdk_data["p2p_percent"] < 99:
            p2p_list.append(sdk_data["id"])

    print "SDK with p2p rate <99%: {0}".format(len(p2p_list))
    print p2p_list


def print_peer_id():
    global sdk_data_list
    peer_id_list = list()
    for sdk_data in sdk_data_list:
        peer_id_list.append(sdk_data["peer_id"])

    print "PEER id LIST"
    print peer_id_list


def collect_p2p_test():
    while True:
        try:
            t1 = time.time()
            # print dash_board_port_list

            global p2p_list, bad_p2p_list, seed_num_list, stream_num_list, bad_stream_list, download_rate_list, bad_cid_list
            global sdk_data_list
            sdk_data_list = list()
            p2p_list = []
            bad_p2p_list = []
            seed_num_list = []
            stream_num_list = []
            bad_stream_list = []
            download_rate_list = []
            bad_cid_list = []

            print SDK_IP_LIST
            for index, ip in enumerate(SDK_IP_LIST):
                # print "start collect p2p for {0}".format(ip)
                # time.sleep(0.1)  # wait some time to start huge threads
                sdk_num = SDK_NUM_LIST[index]
                dash_board_port_list = []
                for i in range(sdk_num):
                    dash_board_port_list.append(SDK_PORT_START + i * SDK_PORT_STEP)
                # print dash_board_port_list

                for port in dash_board_port_list:
                    t = threading.Thread(target=get_sdk_data, args=(ip, port))
                    t.start()
                    t = threading.Thread(target=get_cid_data, args=(ip, port))
                    t.start()
            main_thread = threading.currentThread()
            for t in threading.enumerate():
                if t is not main_thread:
                    t.join()

            t2 = time.time()
            zero_list = [x for x in p2p_list if x == 0]
            non_zero_list = [x for x in p2p_list if x != 0]
            non_zero_download_list = [x for x in download_rate_list if x != 0]
            current = time.localtime()
            time_str = time.strftime("%Y/%m/%d %H:%M:%S", current)
            bad_p2p_list.sort()
            bad_stream_list.sort()

            print "===================================================================================================="
            print "Time: {0} cost {1} seconds to get result".format(time_str, t2 - t1)
            print "IP number is: ", len(SDK_IP_LIST), SDK_IP_LIST
            print_bad_sdk()
            print "SDK number is: {0}".format(len(p2p_list))
            print "------------------------------------------"
            print "          All sdk average p2p is: {0}%".format(sum(p2p_list) / len(p2p_list))
            if len(non_zero_list) != 0:
                print "          Alive sdk average p2p is: {0}%".format(sum(non_zero_list) / len(non_zero_list))
                print "          Max p2p is {0}%, Min p2p is {1}% (>0%)".format(max(non_zero_list), min(non_zero_list))
            print "          {0} SDKs with p2p >= 80%".format(len([i for i in non_zero_list if i >= 80]))
            print "          {0} SDKs with p2p = 0%".format(len(zero_list))
            print "          {0} SDKs is alive".format(len(non_zero_download_list))
            print "------------------------------------------"
            print "          {0} SDKs with seed (0, 32)".format(len([i for i in seed_num_list if i < 32]))
            print "          {0} SDKs with stream >= 32".format(len([i for i in stream_num_list if i >= 32]))
            print "          {0} SDKs with stream (0, 32)".format(len([i for i in stream_num_list if 0 < i < 32]))
            print "          {0} SDKs with stream = 0".format(len([i for i in stream_num_list if i == 0]))
            print "------------------------------------------"
            # print "Download List", download_rate_list
            print "All sdk average download rate {0} kbps".format(sum(download_rate_list) / len(download_rate_list))
            print "Alive sdk average download rate {0} kbps".format(
                sum(download_rate_list) / len(non_zero_download_list))
            print "SDK reading cid has problem ", len(bad_cid_list), bad_cid_list
            print "===================================================================================================="
            # print p2p<99% sdk info
            # print_less_99_sdk()
            print "===================================================================================================="
            # print all peer id
            # print_peer_id()
        except Exception as e:
            traceback.print_exc()
            print e.message
            pass

        time.sleep(15)


def get_url_start_end(ip):
    index = SDK_IP_LIST.index(ip)
    start = sum(SDK_NUM_LIST[:index])
    end = sum(SDK_NUM_LIST[:index + 1])
    return start, end


###############################
# Main Function
###############################
if __name__ == "__main__":
    mutex = threading.Lock()

    sdk_data_list = list()

    p2p_list = []
    bad_p2p_list = []
    seed_num_list = []
    stream_num_list = []
    bad_stream_list = []
    download_rate_list = []
    bad_cid_list = []
    cid_dict = dict()

    time1 = time.time()
    tester = Tester()

    if len(sys.argv) < 2:
        tester.print_help()
    else:
        if len(sys.argv) == 3:
            INI_FILE = sys.argv[2]

        else:
            INI_FILE = "host.ini"
        INI_FILE_PATH = "{0}/{1}".format(parent_path, INI_FILE)

        read_ini()

        # if replace all the files, need to confirm
        if sys.argv[1] == "start":
            answer = raw_input("Attention: <start> remove all data, Y/y for confirm\n")
            answer = str.upper(answer)
            if answer == "Y" or answer == "YES":
                print("You chose start.")
                time.sleep(1)
                tester.start_sdk_test()
            else:
                print("You cancelled.")
        elif sys.argv[1] == "restart":  # skip deploy sdk steps to save time
            tester.restart_sdk_test()
        elif sys.argv[1] == "stop":  # stop sdk, stop play
            tester.stop_sdk_test()
        elif sys.argv[1] == "deploy":
            tester.deploy_test()
        elif sys.argv[1] == "clean":  # delete live and player files
            tester.clean_test()
        elif sys.argv[1] == "core":  # find core dump file for sdk
            print "Now, we will search core dump files"
            tester.core_test()
        elif sys.argv[1] == "version":  # find core dump file for sdk
            print "Now, we will check SDK version"
            tester.version_test()
        elif sys.argv[1] == "data":  # find core dump file for sdk
            print "Now, we will search yunshang.data files"
            tester.data_test()
        elif sys.argv[1] == "sdk":  # find alive player process
            print "Now, we will get sdk process number:"
            tester.sdk_test()
        elif sys.argv[1] == "remove_core":  # remove core dump file for sdk
            print "Now, we will remove core dump files"
            tester.remove_core_test()
        elif sys.argv[1] == "remove_data":  # remove data file for sdk
            print "Now, we will remove yunshang.data files"
            tester.remove_data_test()
        elif sys.argv[1] == "p2p":  # collect p2p data for sdks
            collect_p2p_test()
        elif sys.argv[1] == "done":  # collect p2p data for sdks
            tester.done_test()
        elif sys.argv[1] == "replace_sdk":
            print "Now, we will replace ys_service_static files"
            tester.replace_sdk_test()
        else:
            tester.print_help()

    time2 = time.time()
    print "********** Cost {0} seconds **********".format(time2 - time1)
