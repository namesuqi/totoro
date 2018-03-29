# coding=utf-8
# author: zengyuetian
# unzip tar.gz which downloaded from jenkins build
# replace the dir according to your folder structure

import os
from libs.common.tar_file import *

if __name__ == "__main__":
    """
    place tar.gz under download_dir
    program will unzip your tar.gz to extract_dir
    delete tag.gz
    and delete useless shell
    """
    import glob

    download_dir = r"D:\zDownload"
    extract_dir = download_dir + r"\extract"
    # delete older extract files
    cmd = r"DEL /Q /S {0}\*".format(extract_dir)
    print cmd

    os.system(cmd)

    gz_files = glob.glob(download_dir + "/*.tar.gz")
    for f in gz_files:
        print f
        untar(f, extract_dir)

    # delete sh and tar
    cmd = r"DEL /Q /S {0}\*.sh".format(extract_dir)
    print cmd
    os.system(cmd)

    # delete older tar.gz files
    cmd = r"DEL /Q /S {0}\*.tar.gz".format(download_dir)
    print cmd
    os.system(cmd)

    # z = ZFile("D:/Personal/Downloads/archive.zip")
    # z.extract_to("E:/")
