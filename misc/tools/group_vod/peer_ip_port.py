# coding=utf-8
# author=zengyuetian
# get peer id according to host.ini

import json
import requests
import threading
import time
import os
import inspect
import sys
import ConfigParser
SDK_PORT_START = 30000
SDK_PORT_STEP = 10


# get current dir path
file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
parent_path = os.path.dirname(file_path)
INI_FILE = 'host.ini'
mutex = threading.Lock()
peer_ids = list()


def get_id_by_ajax(ip, num, port):
    peer_ids = list()
    distance = 0
    for i in range(num):
        t = threading.Thread(target=get_peer_id, args=(ip, port + distance))
        t.start()
        time.sleep(0.01)
        distance += SDK_PORT_STEP

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    return peer_ids


def get_peer_id(ip, port):
    print(ip, port)
    url = "http://{0}:{1}{2}".format(ip, port, "/ajax/conf")
    headers = dict()
    headers["accept"] = 'application/json'
    headers["content-type"] = 'application/json'
    res = requests.get(url, headers=headers, timeout=5)
    peer_id = json.loads(res.content).get("peer_id", None)

    url = "http://{0}:{1}{2}".format(ip, port, "/ajax/login")
    headers = dict()
    headers["accept"] = 'application/json'
    headers["content-type"] = 'application/json'
    res = requests.get(url, headers=headers, timeout=5)
    ip = json.loads(res.content).get("publicIP", None)
    port = json.loads(res.content).get("publicPort", None)

    if mutex.acquire(1):
        peer_info = list()
        peer_info.append(peer_id)
        peer_info.append(ip)
        peer_info.append(port)
        peer_ids.append(peer_info)
        mutex.release()


def read_ini():
    """
    get configure info from ini file
    :return: None
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open(INI_FILE_PATH))
    section_list = config.sections()
    for i in section_list:
        if config.has_section(i):
            SDK_IP_LIST.append(config.get(i, "IP"))
            SDK_NUM_LIST.append(int(config.get(i, "SDK_Number")))
        else:
            break

if __name__ == "__main__":
    SDK_IP_LIST = []
    SDK_NUM_LIST = []

    INI_FILE_PATH = "{0}/{1}".format(parent_path, INI_FILE)

    read_ini()
    print SDK_IP_LIST
    start_time = time.time()

    for index, ip in enumerate(SDK_IP_LIST):
        num = SDK_NUM_LIST[index]
        ids = get_id_by_ajax(ip, num, SDK_PORT_START)

    print peer_ids
    end_time = time.time()

    fp = file('id_ip_port.txt', 'w')
    json.dump(peer_ids, fp)
    fp.close()

    print("Get peer id num: {0}".format(len(peer_ids)))
    print("Please check id.txt for peer ids.")
    print("Done, cost {0} seconds.".format(end_time-start_time))
