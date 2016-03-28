#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: Klin
@license: Apache Licence 
@contact: lijian.klin@gmail.com
@site: http://www.cnblogs.com/l33klin/
@software: PyCharm
@file: download_files.py
@time: 16/3/19 上午11:04
"""
import threading
import Queue
import time
import os
import sys
import urllib2
import logging
import traceback

sys.path.append('..')
import log

_lq_lock = threading.Lock()
_links_queue = Queue.Queue()
_failed_queue = Queue.Queue()

_success_list_lock = threading.Lock()
_success_list = list()
_fail_list_lock = threading.Lock()
_fail_list = list()
_download_success_file = 'download_success_links'
_download_fail_file = 'download_fail_links'


class SmallFileDownloader(threading.Thread):
    """
    小文件下载器，从队列中读取下载链接顺序下载，动态的将下载成功或者失败的链接写入到成功失败的文件中
    """

    def __init__(self, thread_name='', duration=1, timeout=3, retry_times=0, out_path=''):
        threading.Thread.__init__(self)
        self.thread_name = thread_name

        self.download_duration = duration
        self.timeout = timeout
        self.retry_times = retry_times
        self.out_path = out_path

    def run(self):
        while True:
            link = ''
            q_empty = False
            _lq_lock.acquire()
            if not _links_queue.empty():
                link = _links_queue.get()
                logging.info('%s start to download:%s' % (self.thread_name, link))
            else:
                q_empty = True
            _lq_lock.release()

            if q_empty:  # 如果队列为空则跳出循环
                break

            if not is_link_downloaded(link):
                if self.download(link, retry_times=self.retry_times):
                    add_to_success(link)
                else:
                    add_to_fail(link)
            else:
                logging.info('%s: %s already downloaded' % (self.thread_name, link))

            time.sleep(self.download_duration)
        logging.info('%s exiting...' % self.thread_name)
        pass

    def download(self, link, filename=None, retry_times=0):
        """
        下载文件
        :param link:待下载的链接
        :param filename:保持的文件名，文件路径为self.out_path
        :param retry_times:重试次数
        :return:
        """
        success = True
        download_times = 0
        while download_times <= retry_times:
            try:
                resp = urllib2.urlopen(link, timeout=self.timeout)
                if filename is None:
                    filename = link.split('/')[-1]
                file_path = os.path.join(self.out_path, filename)
                if os.path.exists(file_path):
                    logging.warning("Warning: %s is exists!" % file_path)
                with open(file_path, 'wb') as f:
                    f.write(resp.read())
                success = True
                break
            except Exception as e:
                success = False
                logging.error(e.message)
                logging.error(traceback.__all__)
                logging.warning('%s download failed try again...' % self.thread_name)
            download_times += 1

        return success


def add_to_success(link):
    """
    把链接添加到成功列表同时写入下载成功文件
    """
    _success_list_lock.acquire()
    _success_list.append(link)
    try:
        with open(_download_success_file, 'a') as f:
            f.write(link + '\n')
            f.flush()
    except Exception as e:
        logging.error('Error: %s' % e.message)
        logging.error(traceback.__all__)
    _success_list_lock.release()
    pass


def add_to_fail(link):
    """
    把链接添加到失败列表同时写入下载失败文件
    """
    _fail_list_lock.acquire()
    _fail_list.append(link)
    try:
        # print 'write %s to fail file!' % link
        with open(_download_fail_file, 'a') as f:
            f.write(link + '\n')
            f.flush()
    except Exception as e:
        logging.error('Error: %s' % e.message)
        logging.error(traceback.__all__)
    _fail_list_lock.release()
    pass


def is_link_downloaded(link):
    """
    判断链接是否已经下载过
    """
    already_download = False
    _success_list_lock.acquire()
    if link in _success_list:
        already_download = True
    _success_list_lock.release()

    if already_download:
        return already_download

    _fail_list_lock.acquire()
    if link in _fail_list:
        already_download = True
    _fail_list_lock.release()

    return already_download


def load_urls(file_path):
    """
    将文件中的下载链接读入一个队列中
    :param file_path:
    :return:
    """
    urls = list()
    if not os.path.exists(file_path):
        return list()
    with open(file_path, 'r') as f:
        line = f.readline()
        while line:
            line_dat = line.strip()
            if line_dat != '':
                urls.append(line_dat)
            line = f.readline()
    return urls


def init(url_file):
    """
    初始化：将urls文件中的链接读入待下载队列
    :return:
    """
    # 初始化下载成功的文件列表
    global _success_list
    _success_list = load_urls(_download_success_file)

    urls = load_urls(url_file)
    for url in urls:
        _links_queue.put(url)

    pass


# def save_fail_links(file_path):
#     """
#     保存失败列表到文件
#     :return:
#     """
#     with open(file_path, 'w') as f:
#         while not _failed_queue.empty():
#             link = _failed_queue.get()
#             f.write(link + '\n')
#             f.flush()
#     pass


def main():
    url_file = 'file_links'
    # fail_file = 'download_fail_links'
    thread_count = 3
    download_duration = 5
    download_timeout = 10
    retry_times = 3
    out_path = 'raw_gz_file'

    init(url_file)

    thread_list = list()
    for i in range(thread_count):  # 创建线程池去下载文件
        thread = SmallFileDownloader(thread_name='Thread-%d' % i,
                                     duration=download_duration,
                                     timeout=download_timeout,
                                     retry_times=retry_times,
                                     out_path=out_path)
        thread.start()
        thread_list.append(thread)

    while True:
        if _links_queue.empty():  # 如果队列中的链接都下载完成了则结束循环
            break
        for i in range(len(thread_list)):  # 遍历线程列表重启挂掉的线程
            if not thread_list[i].isAlive():
                logging.warning('%s is dead. Restarting...')
                th_name = thread_list[i].thread_name
                thread_list[i].join()
                new_thread = SmallFileDownloader(thread_name='%s' % th_name,
                                                 duration=download_duration,
                                                 timeout=download_timeout,
                                                 retry_times=retry_times,
                                                 out_path=out_path)
                new_thread.start()
                thread_list[i] = new_thread

        time.sleep(5)

    for thread in thread_list:
        thread.join()

    # save_fail_links(fail_file)  # 已增加动态写入失败文件的方法，去掉最后一起写入的方法
    logging.info('Exiting main thread...')


if __name__ == '__main__':
    # url = 'http://1usagov.measuredvoice.com/bitly_archive/usagov_bitly_data2011-12-31-1325374229.gzXXX'
    # path = os.path.join('raw_gz_file', 'usagov_bitly_data2011-12-31-1325374229.gz')
    # resp = urllib2.urlopen(url)
    # print resp.code
    # with open(path, 'wb') as f:
    #     f.write(resp.read())
    log.init_log(log_path='log')
    main()
    pass
