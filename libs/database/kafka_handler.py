#!/usr/bin/python
# -*-coding:UTF-8 -*-
"""
kafka相关操作

 __author__ = 'zsw'

"""
import struct
import avro.schema
import time
import avro.io
import avro.schema
import io
from kafka import KafkaClient, SimpleProducer, SimpleConsumer
from libs.database.kafka_schema import *
from libs.decorator.trace import print_trace


@print_trace
def kafka_consumer(kafka_hosts, schema_host, schema_port, topic, consumer_group="python"):
    """
    消费kafka对应topic的记录, 非实时消费
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
    simple_consumer = SimpleConsumer(client, consumer_group, topic, auto_offset_reset="smallest")
    collect_logs = []  # 存放消息记录的partition，offset，value
    msg_exist = True
    while msg_exist:
        msg = simple_consumer.get_message(get_partition_info=True)
        # print "kafka log:", msg
        # 判断此次获取的记录是否为None，为None则停止消费
        if msg is None:
            msg_exist = False
        else:
            msg_partition = msg[0]
            msg_offset = msg[1].offset
            msg_value = msg[1].message.value
            # 对单条记录解码
            bytes_msg = io.BytesIO(msg_value[5:])
            decode_msg = avro.io.BinaryDecoder(bytes_msg)
            recode_msg = avro.io.DatumReader(avro.schema.parse(topic_schema)).read(decode_msg)
            # 收集该log的partition，offset，value信息
            msg_collect = [msg_partition, msg_offset, recode_msg]
            collect_logs.append(msg_collect)
    collect_logs.sort(key=lambda x: x[0])  # 按partition id排序
    print "+++++++Topic: %s+++++++" % topic
    for index, log in enumerate(collect_logs):
        print index, log
    print "Successfully received."
    return collect_logs

    # for message in simple_consumer:
    #     # print type(message)
    #     # print message.offset, message.message.value
    #     # print 'offset: %s' % message.offset, 'data: ' + message.value
    #     bytes_msg = io.BytesIO(message.message.value[5:])
    #     decode_msg = avro.io.BinaryDecoder(bytes_msg)
    #     recode_msg = avro.io.DatumReader(avro.schema.parse(topic_schema)).read(decode_msg)
    #     consumer_logs.append(recode_msg)
    #     print count, message.offset, recode_msg
    #     count += 1
    # return consumer_logs


@print_trace
def kafka_producer(kafka_hosts, schema_host, schema_port, logs, topic, write_time=-9, flag="\x00", **kwargs):
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
    client = KafkaClient(hosts=kafka_hosts)
    simple_producer = SimpleProducer(client)
    if type(logs) != list:
        logs = [logs]
    print "-------Topic: %s-------" % topic
    for index, log in enumerate(logs):
        print index, log
        for k, v in kwargs:
            log[k] = kwargs[k]

        if write_time == -9:
            log["timestamp"] = int(time.time()*1000)
        else:
            log["timestamp"] = int(write_time)

        bytes_encode = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_encode)
        datum_writer = avro.io.DatumWriter(schema)
        datum_writer.write(log, encoder)
        bytes_log = bytes_encode.getvalue()
        bytes_schemaid = struct.pack('>L', topic_schema_id)
        partition = 0
        # simple_producer._send_messages(topic, partition, flag + bytes_schemaid + bytes_log)
        simple_producer.send_messages(topic, flag + bytes_schemaid + bytes_log)

    print "Sent successfully."


if __name__ == "__main__":
    LF_LOG = {"peer_id": "00000002FA7C478F8E04749178FE62A5", "version": "3.5.0", "file_id": "00000002FA7C478F8E04749178FE62A5", "country": "ZZ", "province_id": "0", "city_id": "0", "isp_id": "0", "cppc": 1, "operation": "-", "upload": 0, "download": 0}
    LIVE_LOG = {"peer_id": "00000002FA7C478F8E04749178FE62A5", "version": "3.5.0", "file_id": "00000002FA7C478F8E04749178FE62A5", "country": "ZZ", "province_id": "0", "city_id": "0", "isp_id": "0", "chunk_id": 1, "operation": "-", "cdn": 0, "p2p": 0, "p2penable": True}
    USER_SWITCH_LOG = {"user_id": "00010022", "switch": True, "timestamp": 1}
    k = "192.168.1.230:9092,192.168.1.232:9092,192.168.1.191:9092,192.168.1.189:9092"
    k2 = "kafka-node-1:9092,kafka-node-3:9092,kafka-node-4:9092,kafka-node-5:9092"
    # kafka_producer(k2, "192.168.1.230", 8081, [LF_LOG, LF_LOG], "lf_report")
    # kafka_consumer(k, "192.168.1.230", 8081, "lf_report")

