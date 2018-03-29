# coding=utf-8
# author: Tang Hong
# purpose:
import requests
import math
from libs.common.parse_response import *
from vod_file import *


def get_ajax_lsm():
    res = requests.get(ajax_lsm_url)
    print res
    return res


if __name__ == "__main__":
    vod_files = [file1, file2, file3, file4, file5, file7, file8]
    all_vod_files = [x.get("file_id") for x in vod_files]

    lsm_content = get_ajax_lsm()
    downloaded_file_ids = list()
    files = get_response_data_by_path(lsm_content, "/het")
    for key, file_id in files.items():
        if key != "head" and key != "dirty":
            downloaded_file_ids.append(file_id)
    print("following files are downloaded")
    print downloaded_file_ids
    bet = 0
    for i in downloaded_file_ids:
        for y in vod_files[:7]:
            if i == y.get("file_id"):
                z = y.get("file_size")
                chunk_gross = math.ceil((float(z)/304/1392))
                print "chunk_gross:", chunk_gross
                single_file_bet = 298 + chunk_gross*5
                print "file:", i,  "'s filesize is :", z, ", bet value is :", single_file_bet
                bet = single_file_bet + bet
    print "all files',bet value is:", bet
    meta_size = bet + 864 + 1118368
    print "SDK's yunshang.meta's filesize shoulb be 1118368 + 864 + bet=", meta_size


