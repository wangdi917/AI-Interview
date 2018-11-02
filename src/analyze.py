from __future__ import absolute_import, unicode_literals, print_function, division
import os, sys, argparse
import logging
from autologging import logged
import numpy as np
import pandas as pd
from pandas import DataFrame
import math
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


warnings.filterwarnings("ignore")


dirs = os.listdir("../data/")
print ("All the files in the folder are: {}".format(dirs))
df = pd.read_excel("../data/Java_General.xls")
# print (df.head())

df_general = pd.read_excel("../data/Java_Simple.xls")
index = df_general["用户名"]
general_cols = []
general_cols_simple = []
count = 0
for question in df_general.columns:
    if question[-1] == "？" or question[-2] == "？":
        count += 1
        general_cols.append(question)
        general_cols_simple.append("q" + str(count))

print ("\nFor beginning, the index is:\n{}".format(index))
# 0 张三 | 1 李四
# 2 王五 | 3 刘六
# Name: 用户名, Length: 176, dtype: object

print ("\nFor beginning, the general_cols is:\n{}".format(general_cols))
# ['你为什么考虑应聘陆金所？', '你有没有用过陆金所APP？你对陆金所APP有什么建议吗？', '有没有利用业务时间做过小软件、小程序或者小插件？实现了什样的功能？']
print ("\nFor beginning, the general_cols_simple is:\n{}".format(general_cols_simple))
# ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9']

print ("\nBefore slicing, the DF is:\n{}".format(df_general))
# [176 rows x 45 columns]
df_general = df_general.loc[:, general_cols]
# print ("\nAfter slicing, the DF is:\n{}".format(df_general))
'''
    '你为什么考虑应聘陆金所？', '你有没有用过陆金所APP？你对陆金所APP有什么建议吗？', '有没有利用业务时间做过小软件、小程序或者小插件？实现了什样的功能？'
0       其他公司不要我……                           有，太烂了！                              你管我？
1       妹子多。                                    没有，太烂了！                         急着泡妹子。
[176 rows x 9 columns]
'''

df_general.columns = general_cols_simple
df_general.index = index
# print ("\nAfter appointing, the DF is:\n{}".format(df_general))
'''
用户名     q1,             q2,         q3, ...
张三      其他公司不要我……   有，太烂了！      你管我？
李四      妹子多。            没有，太烂了！ 急着泡妹子。
[176 rows x 9 columns]
'''


def what_is_the_general_question(q):
	return general_cols[general_cols_simple.index(q)]

def match_general_question(q, re_list):
	print("问题:", what_is_the_general_question(q))
	# 问题: 请问你如何看待测试和开发的关系？如果发生矛盾你会如何处理？
	sr = df_general[q]
	sr = sr.astype(str)
	print ("\nDo you know the SR?\n{}".format(sr))
	'''
	用户名      （空的！）
	张三      其他公司不要我……
	李四      妹子多。
	Name: q7, Length: 176, dtype: object
	'''
	sr_match = sr.copy()
	sr_match[:] = False

	for pattern in re_list:
		is_match = sr.apply(lambda x: len(re.findall(pattern, x))>0)
		sr_match += is_match
	print ("\nDo you know the sr_match?\n{}".format(sr_match))
	'''
	用户名      （空的！）
	张三      True
	李四      False
	Name: q7, Length: 176, dtype: bool
	'''
	print("\n匹配率：", str(round(len(sr_match[sr_match])/len(sr_match) * 100, ndigits=2)) + "%")
	print("\n", sr[sr_match == False].values)
	'''
	匹配率： 93.18%
	['开发与测试。' '不熟悉测试' '测试是帮助开发进行高效工作的，最终目标双方是一致的。有矛盾应该基于项目背景来处理。' '没有和测试做过'
	'1+1>2的关系' '以事实说话' '没有测试' '测试和开发应该one team'
	'测试辅助开发，一同完成项目，发生矛盾看实际应该是什么样的' '矛和盾的关系' '测试帮忙开发提升代码质量，测试是上线前的质量把控防线'
	'测试是对于开发完善，发生矛盾会找到矛盾原因，人性处理']
	'''

re_list = ["沟通|协商|商量|协调|协作|支持|和谐|换位|兄弟|左右手|互补|共生|相互|互相", "就事论事", "对事", "不会", "需求", "保险|保障|保证", "站在对方角度", "合作", "讨论", "如果", "解决", "相辅相成", "配合", "具体", "上级|领导"]
match_general_question("q7", re_list)



if __name__ == "__main__":
    print ("\nHello, World!\n")