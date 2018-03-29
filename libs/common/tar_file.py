# coding=utf-8
"""
lib to untar file

__author__ = 'zengyuetian'

"""

import tarfile
import os


def untar(filename, dir):
    t = tarfile.open(filename)
    t.extractall(path=dir)


def tar(filename):
    t = tarfile.open(filename + ".tar.gz", "w:gz")
    for root, dir, files in os.walk(filename):
        print root, dir, files
        for file in files:
            full_path = os.path.join(root, file)
            t.add(full_path)
    t.close()


if __name__ == "__main__":
    untar('E:/archive/COMMON/build/linux/ys-service-3.0.0-centos-base-x86-x86_64-201606210937.tar.gz', 'e:/centos')
