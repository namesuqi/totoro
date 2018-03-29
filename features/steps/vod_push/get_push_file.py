# coding=utf-8
# author: zhangshuwei

import time
from libs.request.header_data import *
from libs.request.http_request import *
from libs.request.http_method import *


def get_push_file(host, port, file_id, start_chunk_id, chunk_num, piece_num):
    """
    sdk -> vod-push, download file data
    :param host:
    :param port:
    :param file_id:
    :param start_chunk_id:
    :param chunk_num:
    :param piece_num: 
    :return:
    """

    url = "/push/files/{0}/chunks/{1}_{2}/pieces/{3}".format(file_id, start_chunk_id, chunk_num, piece_num)

    headers = HeaderData().Content__Type('application/json').ACCEPT('application/json').get_res()

    response = send_http_request(
        GET,
        host,
        port,
        url,
        headers,
        None,
        None
    )
    return response


if __name__ == "__main__":
    fid = "F29264AE593E4DF6B02D49ECD5009996"
    fid2 = "CDA7CA6691544ECABF53220159E81A55"
    fid3 = "C01CC8A4CF6B4DF7AE7BF75E235D1105"
    fid4 = "689798C82AAD47C6A6123765555F5889"
    fid5 = "C412D256C44146E4A60CD7A070020072"
    res_c = []
    res_c2 = []
    # while True:
    for block_id in range(0, 100, 1):
        chunk_id = block_id
        # res = get_push_file("172.30.0.33", 9529, fid2, chunk_id, 1, 1)
        res2 = get_push_file("172.30.0.33", 9529, fid5, chunk_id, 1, 1)
        res_c.append("{0}_{1}: {2}".format(block_id, res2.status_code, res2.headers))
        # print "**************************************bid:",
        # if res.status_code != 200:
        #     break
        # time.sleep(0.5)
    for i in res_c:
        print i
    # print time.ctime()
    # time.sleep(180)
    # time.sleep(10)
    # for block_id in range(0, 460, 1):
    #     chunk_id = block_id * 4
    #     res = get_push_file("172.30.0.33", 9529, fid, chunk_id, 1, 1)
    #     res_c.append("{0}_{1}: {2}".format(block_id, res.status_code, res.headers))
    #     res2 = get_push_file("172.30.0.33", 9529, fid3, chunk_id, 1, 1)
    #     res_c2.append("{0}_{1}: {2}".format(block_id, res2.status_code, res2.headers))
    #     time.sleep(1)
    # for i in res_c:
    #     print i
    # for i in res_c2:
    #     print i

    # for block_id in range(0, 400, 1):
    #     chunk_id = block_id * 3
    #     res2 = get_push_file("172.30.0.33", 9529, fid4, chunk_id, 1, 1)
        # res_c2.append("{0}_{1}: {2}".format(block_id, res2.status_code, res2.headers))
        # print "**************************************bid:",
        # if res.status_code != 200:
        #     break
        # time.sleep(0.5)
    # for i in res_c:
    #     print i
    #
    # for block_id in range(100, 115, 1):
    #     chunk_id = block_id * 3
    #     res2 = get_push_file("172.30.0.33", 9529, fid2, chunk_id, 1, 1)
    #     res_c2.append("{0}_{1}: {2}".format(block_id, res2.status_code, res2.headers))
    #     # print "**************************************bid:",
    #     # if res.status_code != 200:
    #     #     break
    #     # time.sleep(0.5)
    # for i in res_c:
    #     print i