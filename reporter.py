# coding=utf-8
# author: zengyuetian

from libs.common.path import *
import glob


if __name__ == "__main__":
    junit2html = "C:/Python27/Scripts/junit2html"
    print(REPORT_PATH)

    xmls = glob.glob(REPORT_PATH+"/*.xml")
    for xml in xmls:
        cmd = "python {0} {1}".format(junit2html, xml)
        os.system(cmd)


