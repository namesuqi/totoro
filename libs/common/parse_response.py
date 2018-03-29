# coding=utf-8
# __author__ = 'Zeng YueTian'

"""
分析响应的核心库
modified by dh 2016.08.10
"""


def get_response_data_by_path(response, path=None):
    """
    通过path来解析测试框架发送给mock服务器的数据项
    :param response: 发送的api数据列表
    :param path: 路径，通过/分割，数字表示数组中的项
    :return:path指定的数据内容
    """
    # 判断response的内容和path是否为空
    if len(response.content):
        data = response.json()
        if path is not None:
            # 如果是/开头，去掉/；如果path为空，直接返回response中内容
            if path.startswith("/"):
                path = path[1:]
            key_list = path.split("/")

            for key in key_list:
                if key.isdigit():   # 是数组
                    index = int(key)
                    if len(data) != 0:
                        data = data[index]
                    else:
                        data = ""  # 空数组
                else:  # 是key
                    data = data.get(key)
    else:
        data = response.content

    return data






