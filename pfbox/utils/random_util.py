# coding: utf-8
"""
随机数相关
"""
import time

# twitter's snowflake parameters
twepoch = 1288834974657L
datacenter_id_bits = 5L
worker_id_bits = 5L
sequence_id_bits = 12L
max_datacenter_id = 1 << datacenter_id_bits
max_worker_id = 1 << worker_id_bits
max_sequence_id = 1 << sequence_id_bits
max_timestamp = 1 << (64L - datacenter_id_bits - worker_id_bits - sequence_id_bits)
last_timestamp = time.time()
sequence_id = 0
import threading

sss = set()


def make_snowflake(timestamp_ms, sequence_id, datacenter_id=0, worker_id=0, twepoch=twepoch):
    """generate a twitter-snowflake id, based on
    https://github.com/twitter/snowflake/blob/master/src/main/scala/com/twitter/service/snowflake/IdWorker.scala
    :param: timestamp_ms time since UNIX epoch in milliseconds"""

    sid = ((int(timestamp_ms) + twepoch) % max_timestamp) << datacenter_id_bits << worker_id_bits << sequence_id_bits
    sid += (datacenter_id % max_datacenter_id) << worker_id_bits << sequence_id_bits
    sid += (worker_id % max_worker_id) << sequence_id_bits
    sid += sequence_id % max_sequence_id

    sss.add(sid)
    return sid


def until_nex_timestamp():
    while (True):
        now_timestamp = time.time() * 1000
        if now_timestamp > last_timestamp:
            global last_timestamp
            last_timestamp = now_timestamp
            return


def get_sequence_id():
    with threading.Lock():
        global sequence_id
        sequence_id = (sequence_id + 1) % max_sequence_id
        if sequence_id == 0:
            until_nex_timestamp()

        return sequence_id


if __name__ == '__main__':
    import uuid

    start1 = time.time()
    for i in range(100000):
        uuid.uuid4()
    print time.time() - start1

    start = time.time()
    for i in range(100000):
        make_snowflake(time.time()*1000, get_sequence_id())
    print time.time() - start
