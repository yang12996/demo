import  logging
from common.handle_config import conf
import os
from  common.handler_path import LOG_DIR
"""
为了避免程序中创建多个日志收集器而导致日志重复记录，
那么我们可以只创建一个日志收集器，别的模块的使用时都导入这个日志收集器

"""
def create(name="mylog",level="DEBUG",filename="log.log",fh_level="DEBUG",sh_level="DEBUG"):
    #1、创建日志收集器
    log=logging.getLogger(name)

    #第二步:设置收集器收集日志的等级
    log.setLevel(level)

    #第三步:设置输出渠道
    #3.1输出到文件
    fh=logging.FileHandler(filename, encoding="utf-8")
    fh.setLevel(fh_level)
    log.addHandler(fh)

    #3.2输出到控制台
    sh=logging.StreamHandler()
    sh.setLevel(sh_level)
    log.addHandler(sh)


    #第四步:设置日志输出的格式
    #4.1设置日志输出的等级
    formats='%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
    #创建格式对象
    log_format=logging.Formatter(formats)
    # 设置输出到文件的日志格式
    fh.setFormatter(log_format)
    #设置输出到控制台的日志格式
    sh.setFormatter(log_format)

    #返回一个日志收集器
    return log

mylog=create(
            name=conf.get("logging","name"),
            level=conf.get("logging","level"),
            filename=os.path.join(LOG_DIR,conf.get("logging","filename")),
            sh_level=conf.get("logging","sh_level"),
            fh_level=conf.get("logging","fh_level")
)
