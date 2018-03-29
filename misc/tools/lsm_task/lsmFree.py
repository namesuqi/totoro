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


def get_ajax_distribute():
    res = requests.get(ajax_distribute_url)
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
    print("These files have been downloaded or maybe the last file is being downloaded")
    print downloaded_file_ids
    waiting_content = get_ajax_distribute()
    waiting_files_ids = list()
    task_count = get_response_data_by_path(waiting_content, "/task_count")

    # print task_count
    if task_count is 0:
        print "SDK has 0 waiting file"
    else:
        i = 0
        while i < task_count:
            num = str(i)
            path = "/task_list/" + num
            # print path
            waiting_files = get_response_data_by_path(waiting_content, path)
            waiting_file = waiting_files.get("file_id")
            i = i + 1
            waiting_files_ids.append(waiting_file)
        print "These files are waiting to be downloaded or the first file is being downloaded"
        print waiting_files_ids
    # 打印所有不重复的file_id
    all_task_file = waiting_files_ids
    for i in waiting_files_ids:
        if i not in downloaded_file_ids:
            all_task_file.append(i)
    print "已下载的文件和未下载的文件如下"
    print all_task_file
    data = 0
    for i in all_task_file:
        for y in vod_files[:7]:
            if i == y.get("file_id"):
                z = y.get("file_size")
                chunk_gross = math.ceil((float(z) / 304 / 1392))
                print "chunk_gross:", chunk_gross
                single_file_data = chunk_gross*1424
                print "file:", i, "'s filesize is :", z, ", bet value is :", single_file_data
                data = single_file_data + data
    print "all files',data size should be:", data
    print "if all files were downloaded, SDK's yunshang.data's size shoulb be filesize/304/1392/ppc*(1392+32)=", data
    lsmFree = 209715200 - data
    print "lsmFree should be 209715200 -", data, "=", lsmFree