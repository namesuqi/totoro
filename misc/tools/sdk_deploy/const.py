# coding=utf-8
# author=zhangshuwei
# const
from libs.common.path import get_root_path

root_path = get_root_path()
ISO_TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# user and password to access remote machine
ROOT_USER = "root"
ROOT_PASSWD = "root"
ADMIN_USER = "admin"
ADMIN_PASSWD = "admin"

# remote machine ips
REMOTE_IP = "192.168.4.237"

# some default constants
LOG_CONFIG = "myslog.conf"  #
SDK_DEFAULT_FILE = "ys_service_static"
SDK_DEFAULT_PORT = 32717
SDK_PREFIX = 0x00000008
LF_PREFIX = 0x00000009

# sdk location on control machine
LOCAL_SDK_DIR = root_path + "/misc/sdk/linux"
LOCAL_LOG_CONF = root_path + "/misc/sdk/linux/conf/{0}".format(LOG_CONFIG)
RESULT_PATH = root_path + "/result/"

# sdk location on remote machine
SDK_NUM = 20
SDK_PORT_START = 20000
SDK_PORT_STEP = 3
REMOTE_TOTORO_PATH = "/root/totoro"
REMOTE_SDK_PATH = REMOTE_TOTORO_PATH + "/sdk"
REMOTE_CONF_PATH = REMOTE_SDK_PATH + "/conf"
REMOTE_LOG_CONF = REMOTE_CONF_PATH + "/{0}".format(LOG_CONFIG)
REMOTE_SDK = REMOTE_SDK_PATH + "/{0}".format(SDK_DEFAULT_FILE)  #
