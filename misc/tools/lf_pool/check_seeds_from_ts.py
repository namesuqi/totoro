# coding=utf-8
# Author=JKZ
# check seeds from ts
import json
import logging
import requests
import time
from misc.tools.lf_pool.check_ip import checkTaobaoIP

log_file = "stdout.log"
logging.basicConfig(filename=log_file, level=logging.ERROR, format="[%(asctime)s]-%(levelname)s: %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('check_seeds')
logger.setLevel(level=logging.INFO)
logger.addHandler(console)

# TS_HOST = "118.31.134.23:80"  # ONLINE_PRD
TS_HOST = "118.190.120.172:80"  # ONLINE_TEST

HEADERS_SEEDS = {
    "Host": "seeds.crazycdn.com",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/3.19.9"
}

HEADERS_TS = {
    "Host": "ts.crazycdn.com",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/3.19.9"
}

FID_LIST = [
    "E8E757E73DC147E18075F3E07F920F00",  # http://c23.myccdn.info/8adc381069e60d02f203b48c3589251a/5a6eccec/mp4/Avatar.mkv
    "AF2374484EF84A4998E5940A8DFAA564",  # http://c23.myccdn.info/a6d33f8c1bc5dbf00e5b1125d4c62ceb/5a87af7a/mp4/Avatar_15Mbps.mp4
    # "8973145BBAB043B785F9BDEAAF15708B",  # http://c23.myccdn.info/5700a43ee59c295174180064b3819552/5a87b009/mp4/Avatar_20Mbps.mp4
    # "DD328B24A3A54C5DA61D12A7EE3C2D7A",  # http://c23.myccdn.info/60c92d5eca5db242139b1e63b8d1ad41/5a51b856/mp4/piano.mp4
    # "C4BAEFA33AFE4D2EB845988077A05A09",  # http://c23.myccdn.info/b1275d086f4dc9e84a69fe30a6a33ee3/5a728bf0/mp4/Detail_of_the_Earth.mp4
    # "E9FCF99C148347AA9152530779C17C3B",  # http://yunshang.cloutropy.com/demo/middle/demo_9mbps_oled_light.ts
    # "E871E9D1A6A84B01AB9660B4A70E1F2B",  # http://yunshang.cloutropy.com/demo/middle/demo_10mbps_oled_light.ts
    # "20CD44A056F246B892B12F9FB584D564",  # http://yunshang.cloutropy.com/demo/middle/demo_11mbps_piano.ts
]


def get_seeds(peer_id, file_id):
    response = requests.get("http://{0}/getseeds?pid={1}&fid={2}".format(TS_HOST, peer_id, file_id),
                            headers=HEADERS_SEEDS)
    seeds_list = response.json().get("seeds")
    logger.debug("http://seeds.crazycdn.com/getseeds?pid={0}&fid={1}".format(peer_id, file_id))
    logger.debug(seeds_list)
    return seeds_list


def check_seeds(file_seeds):
    ids = dict()
    for i in file_seeds:
        peer_id = i.get("peer_id")
        ids[peer_id] = ids.setdefault(peer_id, 0) + 1

    if len(file_seeds) != len(ids):
        logging.error("".ljust(60, '*') + str(time.ctime()) + " Duplicated !")
        for key, value in ids.items():
            if value > 1:
                logging.error("".ljust(60, '*') + " seed peer_id: "+str(key)+"; count: "+str(value))
        return False
    else:
        return True

if __name__ == "__main__":
    login_body = {
           "version": "4.2.4",
           "natType": 0,
           "publicIP": "116.231.59.90",
           "publicPort": 12345,
           "privateIP": "192.168.2.22",
           "privatePort": 12345,
           "stunIP": "118.31.2.166",
           "macs": {}
    }
    PIDS = [
        "0001002378274C7BB0DECAFBF1575000",
        "0001002378274C7BB0DECAFBF1575001",
        "0001002378274C7BB0DECAFBF1575002"
    ]
    ISP_IPS = {
        "100017": "116.231.59.90",
        "100026": "27.115.0.0",
        "000000": "211.136.173.172"
    }
    i = 0
    isp_pids = {}
    for isp, ip in ISP_IPS.iteritems():
        peer_id = PIDS[i]
        login_body["publicIP"] = ip
        # send login request
        response = requests.post("http://{0}/session/peers/{1}".format(TS_HOST, peer_id),
                                 data=json.dumps(login_body), headers=HEADERS_TS)
        isp_pids[str(isp)] = peer_id
        i += 1
    logger.info("{0}".format(isp_pids))

    while True:
        for peer_id in isp_pids.values():
            # send heartbeat request
            response = requests.get("http://{0}/session/peers/{1}".format(TS_HOST, peer_id), headers=HEADERS_TS)

        # logger.debug("".ljust(60, '-') + str(time.ctime()))
        for fid in FID_LIST:
            for isp, peer_id in isp_pids.iteritems():
                seeds = get_seeds(peer_id=peer_id, file_id=fid)
                try:
                    seeds_count = len(seeds)
                except:
                    seeds_count = 0
                logger.info("Fid: {0}, player isp: {1}, get seeds count: {2}".format(fid, isp, seeds_count))
                if seeds_count != 0:
                    if not check_seeds(seeds):
                        logger.error("Seeds duplicated !!!")
                        logger.error("Fid: {0}, player isp: {1}, paler peer_id: {2}, seeds count: {3}.".format(
                            fid, isp, peer_id, seeds_count))

                    # get isp and province by seed publicIP
                    # s = sorted(seeds, key=lambda seed: seed["publicIP"])
                    # ips = dict()
                    # for i in s:
                    #     pub_ip = i.get("publicIP")
                    #     ips[pub_ip] = ips.setdefault(pub_ip, 0) + 1
                    # for key, value in ips.items():
                    #     if value > 1:
                    #         iploc = checkTaobaoIP(key)
                    #         print value, iploc

        time.sleep(60)

