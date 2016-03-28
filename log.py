#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
####################################################################
"""
Log模块，为整个程序提供log功能

Authors: klin(lijian.klin@gmail.com)
Date:    2015/12/22 14:34
"""

import os
import logging
import logging.handlers


_print_log = True
_log_level = logging.DEBUG


def init_log(log_path, level=_log_level, when="D", backup=7,
             format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
             datefmt="%m-%d %H:%M:%S"):
    """
    init_log - initialize log module

    Args:
      log_path      - Log file path prefix.
                      Log data will go to two files: log_path.log and log_path.log.wf
                      Any non-exist parent directories will be created automatically
      level         - msg above the level will be displayed
                      DEBUG < INFO < WARNING < ERROR < CRITICAL
                      the default value is logging.INFO
      when          - how to split the log file by time interval
                      'S' : Seconds
                      'M' : Minutes
                      'H' : Hours
                      'D' : Days
                      'W' : Week day
                      default value: 'D'
      format        - format of the log
                      default format:
                      %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                      INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
      backup        - how many backup file to keep
                      default value: 7

    Raises:
        OSError: fail to create log directories
        IOError: fail to open log file
    """
    formatter = logging.Formatter(format, datefmt)
    logger = logging.getLogger()
    logger.setLevel(level)

    dir_path = os.path.dirname(log_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf",
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 再创建一个handler，用于输出到控制台
    if _print_log:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(ch)


if __name__ == '__main__':
    init_log("./log/my_program")  # 日志保存到./log/my_program.log和./log/my_program.log.wf，按天切割，保留7天
    logging.debug('debug info')
    logging.info("Hello World!!!")
    logging.warning('warning info')
    logging.error('error info')
    pass
