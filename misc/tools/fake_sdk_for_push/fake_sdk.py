# encoding=utf-8
# Author=JKZ
# 模拟SDK向vod-push请求推送数据，每秒最多发送10次请求，收到503时隔180s或随机1~3min重试，并将记录每次请求信息（时间，chunk_id）
import random
import threading
import math
import requests
import time
import logging
import sys
from conf import *


def fake_sdk(uuid, file_id, chunk_gross, need_random=RETRY_NEED_RANDOM):
    """

    :param uuid: 每个SDK标识，用于日志中区分模拟的SDK
    :param file_id: 文件file_id
    :param chunk_gross: 文件chunk总数
    :param need_random: 重试间隔是否为随机1~3min
    :return:
    """
    start_chunk_id = RAW_START_CHUNK_ID
    while start_chunk_id < chunk_gross:
        if start_chunk_id + CHUNKS_PER_QUERY > chunk_gross:
            last_query_chunks = chunk_gross % CHUNKS_PER_QUERY
            get_file_url = "http://{0}/push/files/{1}/chunks/{2}_{3}/pieces/{4}".format(PUSH_HOST, file_id,
                                                                chunk_gross-last_query_chunks, last_query_chunks, CPPC)
        else:
            get_file_url = "http://{0}/push/files/{1}/chunks/{2}_{3}/pieces/{4}".format(PUSH_HOST, file_id,
                                                                                start_chunk_id, CHUNKS_PER_QUERY, CPPC)

        send_req_time = time.time()
        response = requests.get(get_file_url, headers=HEADERS_PUSH)
        # response = requests.head(get_file_url, headers=HEADERS_PUSH)

        msg = "FID-SDK:{0},{1},{2},{3}".format(uuid, time.time(), start_chunk_id, response.status_code)
        # print msg
        logging.critical(msg=msg)
        if response.status_code == 200:  # 控制fake_sdk每秒至多发送10次请求
            time.sleep(max(0.01, 0.1-(time.time()-send_req_time)))
            start_chunk_id += CHUNKS_PER_QUERY
        elif response.status_code == 503:  # 请求收到503后隔3min重试
            retry_interval = 180-(time.time()-send_req_time)
            if need_random:
                retry_interval = random.randint(60, 180)
            time.sleep(retry_interval)
        else:
            print get_file_url, response.status_code
            logging.critical(msg="ERROR: {0},{1}".format(get_file_url, response.status_code))
            break

if __name__ == "__main__":
    # paras = sys.argv
    sdk_num, fid_no = map(eval, sys.argv[1:])  # str => int
    logging.basicConfig(level=logging.CRITICAL,
                        format='',
                        filename='{0}.log'.format(fid_no),
                        filemode='w')
    f_id, f_size, f_ppc = FILE_INFO_TUPLE
    f_chunk_gross = int(math.ceil(float(f_size)/f_ppc/1392))

    logging.critical(f_id)
    logging.critical("file_size={0}, ppc={1}, chunk_gross={2}".format(f_size, f_ppc, f_chunk_gross))
    threads = list()
    for i in range(sdk_num):
        fid_sdk = "{0}-{1}".format(fid_no, i)
        threads.append(threading.Thread(target=fake_sdk, args=(fid_sdk, f_id, f_chunk_gross,), name=str(i)))
    print time.ctime(), f_id, "start"
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print time.ctime(), f_id, "done"
