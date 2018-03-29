# coding:utf-8

from libs.common.remoter import *
import time
import json

IP = '172.30.0.31'
USER = 'admin'
PASSWORD = 'Yzhxc9!'

REMOTE_FOLDER = "/home/admin/tool/"
LOCAL_FOLDER = "./"
SCRIPT_NAME = "select_file_info.py"
JSON_NAME = "file_info.json"


class get_file_info:

    def __init__(self):
        self.create_folder()
        self.deploy_script()
        self.run_script()
        time.sleep(2)
        self.get_json()
        self.files_info = self.parse_json()

    def __del__(self):
        self.remove_folder()

    def create_folder(self):
        remote_execute(IP, USER, PASSWORD, "mkdir -p {0}".format(REMOTE_FOLDER))

    def deploy_script(self):
        copy_file_to(IP, USER, PASSWORD, "{0}{1}".format(LOCAL_FOLDER, SCRIPT_NAME), "{0}{1}".format(REMOTE_FOLDER, SCRIPT_NAME))

    def run_script(self):
        remote_execute_result(IP, USER, PASSWORD, "python {0}{1}".format(REMOTE_FOLDER, SCRIPT_NAME))

    def get_json(self):
        copy_file_from(IP, USER, PASSWORD, "{0}{1}".format(REMOTE_FOLDER, JSON_NAME), "{0}{1}".format(LOCAL_FOLDER, JSON_NAME))

    def parse_json(self):
        f = file('{0}{1}'.format(LOCAL_FOLDER, JSON_NAME))
        return json.load(f)

    def remove_folder(self):
        remote_execute(IP, USER, PASSWORD, "rm -rf {0}".format(REMOTE_FOLDER))

    def get_file_info(self, file_url):

        for source in self.files_info:
            if source == file_url:
                return self.files_info[source]

        return "file not found"


if __name__ == '__main__':
    pass
