import os
import logging
from .getPath import GetPath


class Log(object):
    def __init__(self, logger=None):
        """
        设置log并指定日志文件
        """
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        # 指定日志路径
        self.log_path = GetPath().get_log_path()
        # 创建一个handler，用于写入日志
        fh = logging.FileHandler(self.log_path, mode='a')
        fh.setLevel(logging.DEBUG)      # 输出到日志的log等级为DEBUG
        # 创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        # 定义两个handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加hanler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger
        
if __name__ == '__main__':
    log = Log(__name__).getlog()
    log.error("测试用例文件不存在！")
