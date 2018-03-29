#!/usr/bin/python
# -*-coding:UTF-8 -*-
"""
kafka相关操作
PyKafka库
 __author__ = 'zsw'

"""

import io
import struct
import avro
import time
from pykafka import KafkaClient
from libs.database.kafka_handler import get_latest_schema_info
from libs.decorator.trace import print_trace


@print_trace
def pykafka_producer(kafka_hosts, schema_host, schema_port, logs, topic, write_time=-9, flag="\x00", **kwargs):
    """
    将log按topic schema写入kafka对应topic中
    :param kafka_hosts:
    :param schema_host:
    :param schema_port:
    :param logs: 一条或多条log
    :param topic: 该log对应topic
    :param write_time: log的timestamp值，为-9时按当前时间戳写入
    :param flag: 标志位，第一个字节是\x00，其他服务以此值校验记录是否正确
    :param kwargs: 对每条log增加或修改key-value
    :return:
    """
    # 获取topic最新schema
    topic_schema, topic_schema_id, schema_version = get_latest_schema_info(schema_host, schema_port, topic)
    schema = avro.schema.parse(topic_schema)
    if type(logs) != list:
        logs = [logs]
    client = KafkaClient(hosts=kafka_hosts)
    kafka_topic = client.topics[topic]

    with kafka_topic.get_sync_producer() as producer:
        print "-------Topic: %s-------" % topic
        for index, log in enumerate(logs):
            # 添加log的timestamp, 默认-9表示ts为当前时间(毫秒级), -7表示不添加timestamp, 其他值表示使用该值作为timestamp
            if write_time == -9:
                log["timestamp"] = int(time.time()*1000)
            elif write_time == -7:
                pass
            else:
                log["timestamp"] = int(write_time)
            # 修改log的部分字段的值
            for k, v in kwargs:
                log[k] = kwargs[k]
            print index, log
            # 将log按照avro schema写入kafka
            bytes_encode = io.BytesIO()
            encoder = avro.io.BinaryEncoder(bytes_encode)
            datum_writer = avro.io.DatumWriter(schema)
            datum_writer.write(log, encoder)
            bytes_log = bytes_encode.getvalue()
            bytes_schemaid = struct.pack('>L', topic_schema_id)
            producer.produce(flag + bytes_schemaid + bytes_log)
    print "Sent successfully."


@print_trace
def pykafka_consumer(kafka_hosts, schema_host, schema_port, topic, consumer_group="python2"):
    """
    消费kafka对应topic的记录
    :param kafka_hosts:
    :param schema_host:
    :param schema_port:
    :param topic:
    :param consumer_group:
    :return:
    """
    # 获取topic最新schema
    topic_schema, topic_schema_id, schema_version = get_latest_schema_info(schema_host, schema_port, topic)
    # 消费kafka记录
    client = KafkaClient(hosts=kafka_hosts)
    kafka_topic = client.topics[topic]

    # print time.asctime(time.localtime(time.time()))
    # print "topic:", topic, "; partitions num:", len(kafka_topic.partitions)
    consumer = kafka_topic.get_simple_consumer(consumer_group=consumer_group,
                                               consumer_timeout_ms=5000,
                                               auto_commit_enable=True,
                                               auto_commit_interval_ms=1,
                                               consumer_id=consumer_group
                                               )
    collect_logs = []  # 存放消息记录的partition，offset，value
    for message in consumer:
        if message is not None:
            msg_partition = message.partition.id
            msg_offset = message.offset
            # 对单条记录解码
            bytes_msg = io.BytesIO(message.value[5:])
            decode_msg = avro.io.BinaryDecoder(bytes_msg)
            recode_msg = avro.io.DatumReader(avro.schema.parse(topic_schema)).read(decode_msg)
            # 收集该log的partition，offset，value信息
            msg_collect = [msg_partition, msg_offset, recode_msg]
            # print msg_collect
            collect_logs.append(msg_collect)
    collect_logs.sort(key=lambda x: x[0])  # 按partition id排序
    print "+++++++Topic: %s+++++++" % topic
    print "logs count:", len(collect_logs)
    for index, log in enumerate(collect_logs):
        # print index
        print index, log
    print "Successfully received."
    return collect_logs


if __name__ == "__main__":
    LF_LOG = {"peer_id": "00000002FA7C478F8E04749178FE62A5", "version": "3.5.0", "file_id": "00000002FA7C478F8E04749178FE62A5", "country": "ZZ", "province_id": "0", "city_id": "0", "isp_id": "0", "cppc": 1, "operation": "-", "upload": 0, "download": 0}
    LIVE_LOG = {"peer_id": "00000002FA7C478F8E04749178FE62A5", "version": "3.5.0", "file_id": "00000002FA7C478F8E04749178FE62A5", "country": "ZZ", "province_id": "0", "city_id": "0", "isp_id": "0", "chunk_id": 1, "operation": "-", "cdn": 0, "p2p": 0, "p2penable": True}
    USER_SWITCH_LOG = {"user_id": "00010022", "switch": True, "timestamp": 1}
    k1 = "192.168.1.230:9092,192.168.1.232:9092,192.168.1.191:9092,192.168.1.189:9092"
    # k2 = "kafka-node-1:9092,kafka-node-2:9092,kafka-node-3:9092"
    # k3 = "192.168.1.230:9092,192.168.1.232:9092,192.168.1.191:9092,192.168.1.189:9092"
    # pykafka_producer(KAFKA_HOST, "192.168.4.230", 8081, [LF_LOG, LF_LOG], "lf_report")
    # print zlib.crc32(LF_LOG["peer_id"])%6
    topic_list = ["user_strategy_switch", "channel_strategy_switch", "heartbeat", "lf_report", "peer_info", "live_report"]

    # ALL_NUM = 0
    # for i in range(1000):
    #     for t in topic_list:
    #         kafka_logs = pykafka_consumer(KAFKA_HOST, "192.168.4.230", 8081, t)
    #         ALL_NUM += len(kafka_logs)
    #         print "ALL NUM:", ALL_NUM
    #         try:
    #             print time.asctime(time.localtime(time.time()))
    #             print judge_logs_partition(kafka_logs)
    #         except:
    #             pass
    #         # time.sleep(10)

