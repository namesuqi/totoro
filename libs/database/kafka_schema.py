#!/usr/bin/python
# -*-coding:UTF-8 -*-
"""
schema相关操作

 __author__ = 'zsw'

"""
import requests


def get_latest_schema_info(schema_host, schema_port, topic):
    """
    从服务器获取topic最新信息
    :param schema_host:
    :param schema_port:
    :param topic:
    :return:
    """
    if topic.endswith("-value"):
        topic = topic
    else:
        topic = "{0}-value".format(topic)
    r = requests.get("http://{0}:{1}/subjects/".format(schema_host, schema_port) + topic + "/versions/latest")
    r_json = r.json()
    # print r_json
    schema_id = r_json.get("id", None)
    schema = r_json.get("schema", None)
    schema_version = r_json.get("version", None)
    return schema, schema_id, schema_version


def get_special_schema_by_id(schema_host, schema_port, schema_id):
    """
    根据schema_id获取指定schema
    :param schema_host:
    :param schema_port:
    :param schema_id:
    :return:
    """
    r = requests.get("http://{0}:{1}/schemas/ids/".format(schema_host, schema_port) + str(schema_id))
    r_json = r.json()
    # print "schema_id:", schema_id, ", schema:", r_json["schema"]
    result = r_json.get("schema", None)
    return result


def get_subjects(schema_host, schema_port):
    """
    获取所有subjects
    :param schema_host:
    :param schema_port:
    :return:
    """
    r = requests.get("http://{0}:{1}/subjects".format(schema_host, schema_port))
    # print "subjects:", r.json()
    result = r.json()
    return result


if __name__ == "__main__":
    subjects = get_subjects("192.168.1.230", 8081)
    for subject in subjects:
        schema_info = get_latest_schema_info("192.168.1.230", 8081, subject)

        # print schema_info[0]
        # if "peer_id" in schema_info[0]:
        #     print "********:", subject
        #     print schema_info
        # else:
        #     pass
