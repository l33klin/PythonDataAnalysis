#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
"""
This module provide configure file management service in i18n environment.

Authors: lijian16(lijian16@baidu.com)
Date:    2016/3/17 21:20
"""

import json
import time
import os
from collections import defaultdict
from collections import Counter

import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt  # 导入画图的库


def get_counts(sequence):
    """
    统计序列中元素出现的次数，返回一个元素对应次数的字典
    :param sequence: 需要统计的序列
    :return: 序列元素对应出现次数的字典
    """
    counts = defaultdict(int)  # 所有值会被初始化为0
    for x in sequence:
        counts[x] += 1
    return counts


def top_counts(count_dict, n=10):
    """
    输出统计字典中前n位的统计值字典
    :param count_dict:
    :param n:
    :return:
    """
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]


def count_fun1(records):
    """
    使用自己实现的方法来统计和排序
    :param records:
    :return:
    """
    time_zones = [rec['tz'] for rec in records if 'tz' in rec]
    counts = get_counts(time_zones)
    print top_counts(counts)


def count_fun2(records):
    """
    使用Python Collections库进行统计排序
    :param records:
    :return:
    """
    time_zones = [rec['tz'] for rec in records if 'tz' in rec]
    counts = Counter(time_zones)
    print counts.most_common(10)


def count_fun3(records):
    """
    使用pandas库进行统计排序
    :param records:
    :return:
    """
    frame = DataFrame(records)
    clean_tz = frame['tz'].fillna('Missing')  # 对没有tz字段的数据以Missing代替
    clean_tz[clean_tz == ''] = 'Unknown'  # 把tz值为空的用Unknown代替
    tz_counts = clean_tz.value_counts()
    print tz_counts[:10]
    tz_counts[:10].plot(kind='barh', rot=0)
    plt.show()
    pass


def count_fun4(recrods):

    frame = DataFrame(recrods)
    results = Series([x.split()[0] for x in frame.a.dropna()])
    print results[:5]
    counts = results.value_counts()[:10]
    counts.plot(kind='barh', rot=0)
    plt.show()


if __name__ == '__main__':
    path = os.path.join('data', 'usagov_bitly_data2011-06-02-1307035796')
    records = [json.loads(line) for line in open(path)]

    time_list = []

    # start = time.clock()
    # count_fun1(records)
    # end = time.clock()
    # time_list.append(end - start)
    #
    # start = time.clock()
    # count_fun2(records)
    # end = time.clock()
    # time_list.append(end - start)
    #
    # start = time.clock()
    # count_fun3(records)
    # end = time.clock()
    # time_list.append(end - start)

    start = time.clock()
    count_fun4(records)
    end = time.clock()
    time_list.append(end - start)

    for i in range(len(time_list)):
        print 'Fun%d use time: %f s' % (i+1, time_list[i])

    pass
