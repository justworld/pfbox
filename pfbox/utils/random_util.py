# coding: utf-8
"""
随机数相关
"""
import threading
import time


class Singleton(object):
    """
    单例模式简单实现
    """
    _instance = None

    def __new__(cls, *args, **kargs):
        if hasattr(cls, 'thread_lock'):
            with cls.thread_lock:
                if not cls._instance:
                    org = super(Singleton, cls)
                    cls._instance = org.__new__(cls, *args, **kargs)
        else:
            if not cls._instance:
                org = super(Singleton, cls)
                cls._instance = org.__new__(cls, *args, **kargs)

        return cls._instance


class SnowFlaskID(Singleton):
    """
    https://github.com/twitter/snowflake/blob/master/src/main/scala/com/twitter/service/snowflake/IdWorker.scala
    twitter-snowflake算法实现, 生成19位(目前数据库最大支持数字位数为19)纯数字分布式唯一ID
    64位二进制, 前42为毫秒时间戳, 接下来2位代表版本, 接下来8位代表机器id, 剩余12位代表1毫秒可生成4096个ID
    64位可支持到2150年, 可支持256台服务器每毫秒同时生成4096个不同ID
    相比与uuid, 纯数字、位数更少且趋势递增对数据库友好, 生成更快、数据库性能更好
    单例实现
    """
    # 基础时间戳, 保证ID为19位
    twepoch = 1288834974657
    # 版本位, 用于解决时间回调问题, 支持4个不同版本
    version_bits = 2
    max_version = 1 << version_bits
    # 时间回调问题极少几率出现, 可忽略
    version = 0

    # 机器位, 保证不同服务器生成不同id, 支持256台服务器
    mac_id_bits = 8
    max_mac_id = 1 << mac_id_bits
    # 机器id, 不同服务器该值需保证不一样, 最大为256
    mac_id = 0

    # 序列数位, 同一毫秒下依次增加, 最大为4096, 超过了会等到下一毫秒生成
    sequence_id_bits = 12
    max_sequence_id = 1 << sequence_id_bits
    sequence_id = 0

    # 时间位, 保证不同毫秒生成的ID一定不会重复
    max_timestamp = 1 << (64 - mac_id_bits - sequence_id_bits)
    last_timestamp = time.time() * 1000

    thread_lock = threading.Lock()

    def __init__(self, mac_id):
        print mac_id
        self.mac_id = mac_id

    def get_id(self):
        """
        生成分布式唯一ID
        """
        timestamp_ms = time.time() * 1000
        sid = ((int(
            timestamp_ms) - self.twepoch) % self.max_timestamp) << self.version_bits << self.mac_id_bits << self.sequence_id_bits

        sid += (self.version % self.max_version) << self.version_bits
        sid += (self.mac_id % self.max_mac_id) << self.mac_id_bits
        sid += self._get_sequence_id() % self.max_sequence_id

        return sid

    def _get_sequence_id(self):
        """
        获取序列数, 保证线程安全
        :return:
        """
        with self.thread_lock:
            self.sequence_id = (self.sequence_id + 1) % self.max_sequence_id
            if self.sequence_id == 0:
                self._until_nex_timestamp()

            s2.append(self.sequence_id)
            return self.sequence_id

    def _until_nex_timestamp(self):
        """
        序列数大于4096, 等到下一毫秒生成
        :return:
        """
        while (True):
            now_timestamp = time.time() * 1000
            if now_timestamp > self.last_timestamp:
                self.last_timestamp = now_timestamp
                return
