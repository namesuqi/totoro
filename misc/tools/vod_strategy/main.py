# coding=utf-8
import time
from misc.tools.vod_strategy.const import *
from misc.tools.vod_strategy.basic_request import *
from misc.tools.vod_strategy.scenes_config import REPORT_FILE_SCENES


def sdk_report_file(test_scenes):
    scence_pids = dict()
    for scene, file_info in test_scenes.iteritems():
        file_id = file_info[0]
        peer_num = file_info[1]
        file_status_list = file_info[2]
        print "{0} {1} , sdk num: {2}, {3} {0}".format("".ljust(60, '-'), scene, peer_num, time.ctime())
        peer_id_list = create_peer_id(peer_num)
        for i in range(peer_num):
            peer_id = peer_id_list[i]
            file_status = file_status_list[i % len(file_status_list)]
            print "PEER_ID:" + peer_id + "; FILE_ID: " + file_id + "; FILE_STATUS: " + file_status
            send_login_req(peer_id, DEFAULT_VERSION, DEFAULT_NAT_TYPE, DEFAULT_PUBLIC_IP, DEFAULT_PUBLIC_PORT,
                           DEFAULT_PRIVATE_IP, DEFAULT_PRIVATE_PORT, DEFAULT_STUN_IP, DEFAULT_MACS)
            send_lsm_report(peer_id, file_id, file_status, universe=True, withfile=True)
        scence_pids[scene] = peer_id_list
    return scence_pids


if __name__ == "__main__":

    print sdk_report_file(REPORT_FILE_SCENES)

