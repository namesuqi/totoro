# coding=utf-8
# Author=JKZ
# check seeds of lf pool ( Redis, key: {FOSC_<file_id>_<isp_id>} )
import json
import time
import logging
from rediscluster import StrictRedisCluster

startup_nodes = [{"host": "172.30.0.20", "port": 6379},
                 {"host": "172.30.0.21", "port": 6379},
                 {"host": "172.30.0.22", "port": 6379}]
rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
log_file = "/home/admin/pt_zsw/stdout.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="")

ISP_LIST = ["100017", "100026", "000000"]  # use in FOSC
FID_URL = {
        "96A8329020C446B1A64F0527FB510399": "http://migu.x.00cdn.com/demo/4k/Detail_of_the_Earth.mkv",
        "E8FA6B1181484E95B47A83F32F1971E2": "http://migu.x.00cdn.com/demo/4k/yhtx_offical.mp4",
        "AA675EDFD8CE4C08A6CCAA1B7EA97216": "http://migu.x.00cdn.com/demo/4k/Avatar.mp4",
        "C412D256C44146E4A60CD7A070020072": "http://migu.x.00cdn.com/demo/4k/piano.mp4",
        "6D735CCB90FE46C1AF86C6C82FAB188E": "http://vod4ktest.cloutropy.com/4k/piano.mp4",
        "F25CDCE8686F409BB1ED04BC565A93D0": "http://yunshang.cloutropy.com/demo/4k/Avatar.mp4",
        "E8613034D4964E1ABA9CA0A2237541C9": "http://yunshang.cloutropy.com/demo/4k/piano.mp4",
        "3341AA7443014DF0A21C76784C2459A8": "http://yunshang.cloutropy.com/demo/4k/Detail_of_the_Earth.mp4",
        "A0CC8B40C9A8447ABFABCFAA07FDB9CB": "http://c23.myccdn.info/60c92d5eca5db242139b1e63b8d1ad41/5a51b856/mp4/piano.mp4",
        "300612B1A7D442DE9A215B70FB941BCF": "http://c23.myccdn.info/8adc381069e60d02f203b48c3589251a/5a6eccec/mp4/Avatar.mkv",
        "E6E30B7E972945DB96386CD1DE344CA4": "http://c23.myccdn.info/b1275d086f4dc9e84a69fe30a6a33ee3/5a728bf0/mp4/Detail_of_the_Earth.mp4",
        "9828BE95C7EE42F7964B8ECAAAB12C2B": "http://migu.x.00cdn.com/demo/4k/Detail_of_the_Earth.mp4",
        "85E40D0AB019445CA7D5D413685EB94A": "http://migu.x.00cdn.com/demo/4k/Yellowstone_National_Park_aliyun.mp4",
        "A0A91D34C41F44BDAC68A64D9F1578F0": "http://migu.x.00cdn.com/demo/4k/Interstellar_aliyun.mp4"
    }


def get_file_ids():
    match_keys = rc.keys("*FOSC*")
    file_ids = list()
    for i in match_keys:
        # print i
        split_key = i.split("_")[1:-1]
        fid = "_".join(split_key)
        file_ids.append(fid)

    return list(set(file_ids))


def get_file_all_seeds(file_id):
    file_seeds = list()
    isp_seeds_count = dict()
    if file_id in FID_URL.keys():
        file_url = FID_URL[file_id]
    else:
        file_url = "url is not listed"
    for isp in ISP_LIST:
        fosc_key = "{FOSC_" + str(file_id) + "_" + str(isp) + "}"
        isp_seeds = rc.smembers(fosc_key)
        isp_seeds_count[isp] = len(isp_seeds)
        # print isp, "seeds count:", len(isp_seeds)
        for seed in isp_seeds:
            file_seeds.append(json.loads(seed))

    file_seeds_log = "File_id:"+str(file_id).ljust(32, ' ')+"; seeds count: "+str(len(file_seeds)).ljust(5, ' ')+\
                     str(isp_seeds_count).ljust(45, ' ')+"; "+str(file_url)
    logging.debug(file_seeds_log)

    return file_seeds


def check_seeds(file_seeds, file_id=""):
    ids = dict()
    for i in file_seeds:
        peer_id = i.get("peer_id")
        ids[peer_id] = ids.setdefault(peer_id, 0) + 1
    if len(file_seeds) != len(ids):
        logging.debug("".ljust(60, '*') + " Duplicated ! FILE_ID: "+str(file_id))
        for key, value in ids.items():
            if value > 1:
                # print key
                logging.debug("".ljust(60, '*') + " Peer_id: "+str(key)+"; count: "+str(value))
        return False
    else:
        return True


def part_time_get_fosc(file_id=""):
    match_keys = rc.keys("*" + "FOSC_" + str(file_id) + "*")
    # print match_keys
    file_seeds = dict()
    for i in match_keys:
        # print i
        file_seeds[i] = rc.smembers(i)
    # print file_seeds

    for k,v in file_seeds.iteritems():
        ids = dict()
        print k, "seeds count:", len(v)
        for i in v:
            seed = json.loads(i)
            peer_id = seed.get("peer_id")
            ids[peer_id] = ids.setdefault(peer_id, 0) +1
        print k, "unique seed count:", len(ids)
        if len(v) != len(ids):
            print "*******************************************************Duplicated !"
            for key, value in ids.items():
                if value > 1:
                    print key

if __name__ == "__main__":

    # part_time_get_fosc("7FEFCCCF9C54456D9D9C9DB225967F2E")
    # while True:
    #     print "----------------------------%s--------------------------" % time.ctime()
    #     part_time_get_fosc()
    #     time.sleep(60)
    while True:
        logging.debug("{0} {1} {0}".format("".ljust(80, '-'), time.ctime()))
        file_id_list = get_file_ids()
        for file_id in file_id_list:
            file_seeds = get_file_all_seeds(file_id=file_id)
            check_seeds(file_seeds=file_seeds, file_id=file_id)
        time.sleep(60)
        logging.debug("")
 

