# coding=utf-8
# author: zengyuetian
# only update sdk for 0, 1, n dir
# for vod, keep the data and meta file in yunshang dir
# only run this script on remote sdk machines


import sys
import os
import time

SDK_FILE = 'ys_service_static'

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("please specify sdk number.")
    else:
        num = int(sys.argv[1])
        print("ok, we will replace {0} sdk.".format(num))

        # chmod firstly
        cmd = "chmod 755 {0}".format(SDK_FILE)
        os.system(cmd)

        for i in range(num):
            cmd = "rm -f {0}/{1}; cp {1} {0}".format(i, SDK_FILE)
            os.system(cmd)
            print(cmd)
            time.sleep(0.1)
        print("replace {0} sdk".format(num))






