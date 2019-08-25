# coding: utf-8
"""
随机数相关
"""
import threading
import time
import os


class SnowFlaskID(object):
    """
    https://github.com/twitter/snowflake/blob/master/src/main/scala/com/twitter/service/snowflake/IdWorker.scala
    twitter-snowflake算法实现, 生成19位(目前数据库最大支持数字位数为19)纯数字分布式唯一ID
    64位二进制, 前42为毫秒时间戳, 接下来1位代表版本, 8位代表机器id, 3位代表进程, 剩余10位代表1毫秒可生成1024个ID
    64位可支持到2150年, 可支持256台服务器每台同时8个进程每毫秒同时生成1024个不同ID
    相比与uuid, 纯数字、位数更少且趋势递增对数据库友好, 生成会慢一点但差不多、数据库性能更好
    单例实现, 线程锁保证多线程正常, 文件pid保证多进程正常, 要小心pid文件的数据写入和清空
    """
    # 基础时间戳, 保证ID为19位
    twepoch = 1288834974657

    # 版本位, 用于解决时间回调问题, 支持2个不同版本
    version_bits = 1
    max_version = 1 << version_bits
    # 时间回调问题极少几率出现, 可忽略; 回调version改为1
    version = 0

    # 机器位, 保证不同服务器生成不同id, 支持256台服务器
    mac_id_bits = 8
    max_mac_id = 1 << mac_id_bits
    # 机器id, 不同服务器该值需保证不一样, 最大为256
    mac_id = 0

    # 进程位, 保证同服务器不同进程生成不同id, 每台服务器支持8个进程
    process_bits = 3
    max_process = 1 << process_bits
    # 程序会自动生成process_id
    process_id = 0
    pid = str(os.getpid())

    # 序列数位, 同一毫秒下依次增加, 最大为1024, 超过了会等到下一毫秒生成
    sequence_id_bits = 10
    max_sequence_id = 1 << sequence_id_bits
    sequence_id = 0

    # 时间位, 保证不同毫秒生成的ID一定不会重复
    max_timestamp = 1 << (64 - mac_id_bits - sequence_id_bits)
    last_timestamp = time.time() * 1000

    # 线程锁, 保证不同线程生成不同序列数
    thread_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kargs):
        with cls.thread_lock:
            if not cls._instance:
                org = super(SnowFlaskID, cls)
                cls._instance = org.__new__(cls, *args, **kargs)

                # 清空pid文件, 需要保证先执行这里再生成id
                with open('pid', 'w') as f:
                    f.write('')

        return cls._instance

    def get_id(self):
        """
        生成分布式唯一ID
        """
        process_id = self._get_process_id()
        sequence_id = self._get_sequence_id()

        timestamp_ms = time.time() * 1000
        sid = ((int(timestamp_ms) - self.twepoch) % self.max_timestamp
               ) << self.version_bits << self.mac_id_bits << self.process_bits << self.sequence_id_bits

        sid += (self.version % self.max_version) << self.mac_id_bits << self.process_bits << self.sequence_id_bits
        sid += (self.mac_id % self.max_mac_id) << self.process_bits << self.sequence_id_bits
        sid += (process_id % self.max_process) << self.sequence_id_bits
        sid += sequence_id % self.max_sequence_id

        return sid

    def _get_process_id(self):
        """
        必须动态获取, 比如os.fork()会直接复制数据导致失效
        """
        pid = str(os.getpid())
        if self.pid == pid:
            return self.process_id
        else:
            # 读取pid文件
            with open('pid', 'r') as f:
                data = f.read()

            # 进程id不在pid文件里, 写入再读取
            if pid not in data:
                # 追加进程pid
                with open('pid', 'a') as f:
                    f.write('{},'.format(pid))

                # 避免多进程冲突, 再读取一遍
                with open('pid', 'r') as f:
                    data = f.read()

            data = data.split(',')
            self.process_id = data.index(pid)
            self.pid = pid
            return self.process_id

    def _get_sequence_id(self):
        """
        获取序列数, 保证线程安全
        :return:
        """
        with self.thread_lock:
            self.sequence_id = (self.sequence_id + 1) % self.max_sequence_id
            if self.sequence_id == 0:
                self._until_nex_timestamp()

            return self.sequence_id

    def _until_nex_timestamp(self):
        """
        序列数大于支持, 等到下一毫秒生成
        :return:
        """
        while (True):
            now_timestamp = time.time() * 1000
            if now_timestamp > self.last_timestamp:
                self.last_timestamp = now_timestamp
                return


snow_flask = SnowFlaskID()
