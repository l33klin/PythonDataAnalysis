#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: 
@license: Apache Licence 
@contact: lijian.klin@gmail.com
@site: http://www.cnblogs.com/l33klin/
@software: PyCharm
@file: test_on_MovieLens_data.py
@time: 16/3/22 上午12:32
"""
import os

import pandas as pd


_data_folder = os.path.join('.', 'data', 'ml-1m')
_users_data_file = os.path.join(_data_folder, 'users.dat')
_ratings_data_file = os.path.join(_data_folder, 'ratings.dat')
_movies_data_file = os.path.join(_data_folder, 'movies.dat')

def func():
    pass


class Main(object):
    def __init__(self):
        pass

    def run(self):
        unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
        users = pd.read_table(_users_data_file, sep='::', header=None, names=unames, engine='python')

        rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
        ratings = pd.read_table(_ratings_data_file, sep='::', header=None, names=rnames, engine='python')

        mnames = ['movie_id', 'title', 'genres']
        movies = pd.read_table(_movies_data_file, sep='::', header=None, names=mnames, engine='python')

        print users.head()
        print ratings.head()
        print movies.head()

        data = pd.merge(pd.merge(ratings, users), movies)

        print data[:10]
        # 新旧版本的pivot_table参数不一样，新版中支持多个row（index）
        mean_ratings = data.pivot_table('rating', index=['title'], columns='gender', aggfunc='mean')
        print mean_ratings[:10]
        pass


if __name__ == '__main__':
    main = Main()
    main.run()
    pass
