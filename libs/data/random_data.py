# coding=utf-8
# __author__ = 'liwenxuan'

import random

chars = "1234567890ABCDEF"
ids = ["{0}{1}{2}{3}".format(i, j, k, l) for i in chars for j in chars for k in chars for l in chars]


def random_peer_id(prefix="F"*8, server_id="0000"):
    """
    用于生成随机的peer_id(后四位随机)
    :param prefix: 生成的peer_id的前八位, 测试用prefix为"FFFFFFFF"
    :param server_id: 区分不同server的标识, 不区分server时, server_id为"0000"
    :return:
    """
    assert len(str(prefix)) == 8 and len(str(server_id)) == 4
    return str(prefix) + str(server_id) + "0"*16 + random.choice(ids)  # length: 8+4+16+4 = 32


def random_file_id(file_id_prefix="F"*8, server_id="0000"):
    """
    用于生成随机的file_id(后四位随机)
    :param file_id_prefix: 生成的file_id的前八位, 测试用prefix为"FFFFFFFF"
    :param server_id: 区分不同server的标识, 不区分server时, server_id为"0000"
    :return:
    """
    assert len(str(file_id_prefix)) <= 8 and len(str(server_id)) == 4
    return str(file_id_prefix).ljust(8, "F") + str(server_id) + "F"*16 + random.choice(ids)  # length: 8+4+16+4 = 32


if __name__ == "__main__":
    pass
    print "peer_id", random_peer_id()
    print "file_id", random_file_id()

