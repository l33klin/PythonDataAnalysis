#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: 
@license: Apache Licence 
@contact: lijian.klin@gmail.com
@site: http://www.cnblogs.com/l33klin/
@software: PyCharm
@file: test_on_names_data.py
@time: 16/3/23 上午12:25
"""


# def func():
#     pass
#
#
# class Main(object):
#     def __init__(self):
#         pass
#
#
# if __name__ == '__main__':
#     pass

import pandas as pd
import numpy as np
import os

file_path = os.path.join('data', 'names', 'yob1880.txt')
names1880 = pd.read_csv(file_path, names=['name', 'sex', 'births'])
# names1880

names1880.groupby('sex').births.sum()

years = range(1880, 2015)
pieces = []
columns = ['name', 'sex', 'births']
for year in years:
    path = os.path.join('data', 'names', 'yob%d.txt' % year)
    frame = pd.read_csv(path, names=columns)

    frame['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index=True)

total_births = names.pivot_table('births', index=['year'], columns='sex', aggfunc=sum)

# total_births.plot(title='Total births by sex and year')

def add_prop(group):
    births = group.births.astype(float)

    group['prop'] = births / births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)

# names
# 检查这个分组的总计值是否近似为1
np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]

grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)

pieces1 = []

for year, group in names.groupby(['year', 'sex']):
    pieces1.append(group.sort_values(by='births', ascending=False)[:1000])
top1000 = pd.concat(pieces1, ignore_index=True)

boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

total_births = top1000.pivot_table('births', index=['year'], columns='name', aggfunc=sum)

subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
# 显示几个常见名字出现次数的曲线图
subset.plot(subplots=True, figsize=(12, 10), grid=False, title='Number of births per year')

table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex',
           yticks=np.linspace(0, 1.2, 3), xticks=range(1880, 2020, 10))

# 对占前50%数量的名字的数量变化统计
df = boys[boys.year == 1900]
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
prop_cumsum.searchsorted(0.5) + 1

def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().searchsorted(q)[0] + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
diversity.plot(title="Number of popular names in top 50%")

# 统计最后一个字幕出现的次数
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'

table = names.pivot_table('births', index=last_letters,
                          columns=['sex', 'year'], aggfunc=sum)
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
subtable.head()
letter_prop = subtable / subtable.sum().astype(float)
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)

# 几个常见出现在最后一个字母的变化趋势
letter_prop = table / table.sum().astype(float)
dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T
dny_ts.head()
dny_ts.plot()

# 使用‘Lesley型’名字的男女比例趋势
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
lesley_like

filtered = top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()
table = filtered.pivot_table('births', index='year', columns='sex',
                             aggfunc=sum)
table = table.div(table.sum(1), axis=0)
table.tail()
table.plot(style={'M': 'k-', 'F': 'k--'})
