# coding=utf-8
# author: Tang Hong
# purpose: verify meta hole can be recycled
# steps:
# 1. suppose we have 8 vod files
# 2. download 6 files via sdk
# 3. get file list from lsm ajax
# 4. random select one file to delete
# 5. random select 1 of other 2 file for download
# 6. repeat steps 3-6
import time
import requests
import random
from libs.common.parse_response import *
from vod_file import *


def get_ajax_lsm():
    res = requests.get(ajax_lsm_url)
    return res


def download_file(vod_file):
    file_id = vod_file.get("file_id")
    file_size = vod_file.get("file_size")
    data = [{
        "file_id": file_id,
        "operation": "download",
        "file_size": file_size,
        "piece_size": 1392,
        "ppc": 304,
        "cppc": 1,
        "chunk_num": 4,
        "priority": 1,
        "push_port": 80,
        "push_ip": push_ip,
        "peer_id": peer_id
         }
    ]
    res = requests.post(url, json=data)
    # print res.content


def remove_file(file_id):
    data = [{
        "file_id": file_id,
        "operation": "delete",
        "peer_id": peer_id
    }
    ]
    res = requests.post(url, json=data)
    # print res.content


if __name__ == "__main__":
    vod_files = [file1, file2, file3, file4, file5, file6, file7, file8]
    all_vod_files = [x.get("file_id") for x in vod_files ]
    # prepare download files

    for vod_file in vod_files[:7]:
        download_file(vod_file)
        time.sleep(1)
    time.sleep(3)
    num = 0
    while True:
        num += 1
        print("operation round {0}".format(num))
        print("=================================")

        # get file list from lsm ajax
        lsm_content = get_ajax_lsm()
        downloaded_file_ids = list()
        files = get_response_data_by_path(lsm_content, "/het")
        for key, file_id in files.items():
            if key != "head" and key != "dirty":
                downloaded_file_ids.append(file_id)

        print("following files are downloaded")
        print downloaded_file_ids

        not_downloaded_file_ids = [x for x in all_vod_files if x not in downloaded_file_ids]
        print not_downloaded_file_ids

        # random select one file to delete
        selected_file_id = random.choice(downloaded_file_ids)
        print selected_file_id
        remove_file(selected_file_id)

        # random select one not downloaded file for download
        next_download_file_id = random.choice(not_downloaded_file_ids)
        for temp_file_info in vod_files:
            if temp_file_info.get("file_id") == next_download_file_id:
                file_size = temp_file_info.get("file_size")
                break

        next_download_file_info = {"file_id": next_download_file_id, "file_size": file_size}
        download_file(next_download_file_info)
        time.sleep(60)


