# coding=utf-8
# author: Tang Hong
# purpose: distribute download tasks in random
import requests
from vod_file import *
import time
import random


def download_file(files_list):
    data = list()
    vod_files = [file1, file2, file3, file4, file5, file6, file7]
    for i in files_list:
        for j in vod_files:
            if j.get("file_id") == i:
                file_size = j.values()[3]
                ppc = j.values()[1]
                print ppc
                print file_size
                data.append(
                    {
                        "file_id": i,
                        "operation": "download",
                        "file_size": file_size,
                        "piece_size": 1392,
                        "ppc": ppc,
                        "cppc": cppc,
                        "priority": 1,
                        "push_port": 80,
                        "push_ip": push_ip,
                        "peer_id": peer_id
                    }
                )
        print data
        res = requests.post(url, json=data)


def delete_file(files_list):
    data = list()
    for i in files_list:
        data.append(
            {
                "file_id": i,
                "operation": "delete",
                "peer_id": peer_id
            }
        )
    print data
    res = requests.post(url, json=data)


if __name__ == "__main__":
    files_list = ["21957B9771E94671AB851BA39D9B503C", "80E855957F404713A32222DF6531F64C",
                  "58978B0E0EB84A7AB93A0487D628C44F", "E8E757E73DC147E18075F3E07F920F00",
                  "69FE050B3C1A42BB9FC43A1D36D6B03C", "AF2374484EF84A4998E5940A8DFAA564",
                  "1D4AF9468F9A4E0B9DBAA94ECC5E0212"]
    # print files_list
    while True:
        random.shuffle(files_list)
        print files_list
        download_file(files_list)
        time.sleep(2000)
        delete_file(files_list)
