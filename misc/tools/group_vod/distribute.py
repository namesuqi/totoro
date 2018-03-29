# coding=utf-8
# author: zengyuetian
# tools to distribute task for peer ids

from libs.request.header_data import *
from libs.request.http_request import *
from libs.request.http_method import *
import time

stun_hub_host = "172.30.0.25"
stun_hub_port = 8000

# task info
operation = "download"
push_host = "118.190.153.230"
file_id = "1445FA4CB89E4DA5BDD8BD749DDEB082"
fsize = 775134238
psize = 1392
ppc = 304
cppc = 1
priority = 0
push_port = 80

DOWNLOAD_TASK_PIANO = {"file_id": file_id,
                       "operation": operation,
                       "file_size": fsize,
                       "piece_size": psize,
                       "ppc": ppc,
                       "cppc": cppc,
                       "priority": priority,
                       "push_port": push_port,
                       "push_ip": push_host,
                       "peer_id": None}


def distribute_task(host, port, tasks):
    """
    strategy send distribute task to stub-hub
    :param host:
    :param port:
    :param tasks:task list
    :return: http response
    """

    url = "/distribute_task"

    headers = HeaderData().Content__Type('application/json').ACCEPT('application/json').get_res()
    body_data = tasks

    response = send_http_request(
        POST,
        host,
        port,
        url,
        headers,
        None,
        body_data
    )

    return response


if __name__ == "__main__":

    group_num = 2

    # get peer id from id.txt
    fp = file("id.txt", "r")
    peer_ids = json.load(fp)
    fp.close()
    print(peer_ids)

    index = 1

    # peer_ids = ["00000004D24643C7BF226A561B7FB4CB"]
    for peer_id in peer_ids:
        print(peer_id)

        # init an empty list
        if index % group_num == 1:
            tasks = list()

        task = dict(DOWNLOAD_TASK_PIANO)
        task["peer_id"] = peer_id
        tasks.append(task)

        # send as a group
        if index % group_num == 0:
            resp = distribute_task(stun_hub_host, stun_hub_port, tasks)
        index += 1

        time.sleep(0.05)




