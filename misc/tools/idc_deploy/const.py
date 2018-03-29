# coding=utf-8
# author=zhangshuwei
# const
from libs.common.path import get_root_path

root_path = get_root_path()

SDK_FILE = "ys_service_static"
LOG_CONFIG = "myslog.conf"

TOOL_PATH = root_path + "/misc/tools/idc_deploy"
LOCAL_SDK_FILE = "{0}/{1}".format(TOOL_PATH, SDK_FILE)
LOCAL_LOG_CONF = "{0}/conf/{1}".format(TOOL_PATH, LOG_CONFIG)

IDC_USER_PATH = "/home/admin"
IDC_SDK_PATH = "{0}/vod".format(IDC_USER_PATH)
IDC_SDK_FILE = "{0}/{1}".format(IDC_SDK_PATH, SDK_FILE)
IDC_CONF_PATH = "{0}/conf".format(IDC_SDK_PATH)
IDC_LOG_CONF = "{0}/{1}".format(IDC_CONF_PATH, LOG_CONFIG)

SDK_PREFIX = "0x00010048"
LF_PREFIX = "00010048"

# sdk location on remote machine
SDK_NUM = 20
SDK_PORT_START = 30000
SDK_PORT_STEP = 10


