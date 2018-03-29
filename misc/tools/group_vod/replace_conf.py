# coding=utf-8
# author: zengyuetian
# only update sdk for 0, 1, n dir
# for vod, keep the data and meta file in yunshang dir
# only run this script on remote sdk machines


import sys
import os
import time

conf_dir = 'conf'

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("please specify conf number.")
    else:
        num = int(sys.argv[1])
        print("ok, we will replace {0} conf.".format(num))

        for i in range(num):
            cmd = "rm -rf {0}/{1}; cp -r {1} {0}/".format(i, conf_dir)
            os.system(cmd)
            print(cmd)
            time.sleep(0.1)
        print("replace {0} conf".format(num))






