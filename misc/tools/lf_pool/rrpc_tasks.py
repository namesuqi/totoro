# coding=utf-8
# Author=JKZ
# distribute download tasks and delete tasks to seed repeatedly
import random
import json
import requests
import time
from rediscluster import StrictRedisCluster
import logging

HEADERS_STUN_HUB = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/3.19.9"
}
STUN_HUB_HOST = "172.30.0.25:8000"
startup_nodes = [{"host": "172.30.0.20", "port": 6379},
                 {"host": "172.30.0.21", "port": 6379},
                 {"host": "172.30.0.22", "port": 6379}]

log_file = "stdout.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="[%(asctime)s]-%(levelname)s: %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('rrpc_tasks')
logger.setLevel(level=logging.INFO)
logger.addHandler(console)


def get_online_pids_from_redis(peer_prefix="00010048"):
    rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    match_keys = rc.keys("PNIC_{0}*".format(peer_prefix))
    peer_id_list = list()
    for i in match_keys:
        peer_id = i.replace("PNIC_", "")
        peer_id_list.append(str(peer_id))
    return peer_id_list


def distribute_tasks_to_seed(peer_id, operation, files):
    req_data = []
    for arg in files:
        file_id, file_size, ppc = arg
        task = {
            "file_id": file_id,
            "operation": operation,
            "file_size": file_size,
            "piece_size": 1392,
            "ppc": ppc,
            "cppc": 1,
            "priority": 1,
            "push_port": 80,
            "push_ip": "118.190.153.230",
            "peer_id": peer_id
        }
        req_data.append(task)
    response = requests.post("http://{0}/distribute_task".format(STUN_HUB_HOST), headers=HEADERS_STUN_HUB,
                             data=json.dumps(req_data))
    succ_count = response.json().get("succ_task_count")
    if not succ_count:
        logger.error(
            "Distribute {2} tasks fail. Peer_id: {0}, stun-hub response: {1}".format(peer_id, response.content,
                                                                                     operation))


if __name__ == "__main__":
    f = open("peer_id.txt", 'r')
    file_peer_ids = json.loads(f.readline())
    f.close()

    f_list = [
        ("58978B0E0EB84A7AB93A0487D628C44F", 172917700, 32),
        ("80E855957F404713A32222DF6531F64C", 172917700, 32),
        ("8897CC877C6249BD9F1859CB0C612CA5", 405924148, 176),
        ("1D4AF9468F9A4E0B9DBAA94ECC5E0212", 405924148, 176),
        ("C774E9CA0A9D4D069AC34ECA121955C4", 775134238, 304),
        ("97DB961CBF744EAAA12BE1D949B259A6", 775134238, 304),
        ("3D4CD3E8B21B486EBE743BE4BE6EFFEF", 775134238, 304),
        ("69FE050B3C1A42BB9FC43A1D36D6B03C", 1085532904, 256),
        ("E8E757E73DC147E18075F3E07F920F00", 1447161183, 304),
        ("924EA35C2D024A5992B918651C9AAAD6", 2676689121, 304),
        ("4BC9C6A2352F4D0093F1924C8F08E0E5", 11322052622, 304),
        ("21957B9771E94671AB851BA39D9B503C", 24562731801, 304),
        ("84875C6BEFB34D38A196738CB33222E9", 39238127627, 304),
    ]
    random.shuffle(f_list)
    download_fids = f_list[:4]
    delete_fids = f_list
    peer_ids = file_peer_ids[:200]
    logger.info("Action")
    logger.info("Download files: \n{0}".format(str(download_fids).replace("),", ")\n")))
    logger.info("Delete files: \n{0}".format(str(delete_fids).replace("),", ")\n")))
    while True:
        # peer_ids = get_online_pids_from_redis(peer_prefix="00010048")
        logger.info("Load peer_id num: {0}".format(len(peer_ids)))
        logger.info("Distribute delete task")
        for pid in peer_ids:
            distribute_tasks_to_seed(peer_id=pid, operation="delete", files=delete_fids)
        time.sleep(10)
        logger.info("Distribute download task")
        for pid in peer_ids:
            distribute_tasks_to_seed(peer_id=pid, operation="download", files=download_fids)
        time.sleep(900)
