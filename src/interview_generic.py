from __future__ import absolute_import, unicode_literals, print_function, division
import os, sys, argparse
import logging
from autologging import logged
import numpy as np
import pandas as pd
import re
import copy
import warnings

from const import *


warnings.filterwarnings("ignore")


'''
+-------+---------------+-----------------------+-------------------------------------------------------------------------------------------+
| 用户名	|  UM账号 		| 面向对象的特性有哪些？	| 分布式缓存有哪些应用场景？																	|
+-------+---------------------------------------+-------------------------------------------------------------------------------------------+
| 毕坤	| bikun130		| 我没有对象，怎么面向？	| 存储会话信息；为了缓解db压力从缓存查询提升性能；存储的都是一些不经常变动、对实时性要求不高的数据。	|
| 渠国庆	| quguoqing661	| 封装、继承、多态。		| 1.高性能 2.高qps场景 3.找工作面试场景 4.痛殴产品经理场景 5.和其他程序员聚会派对场景				|
+-------+---------------+-----------------------+-------------------------------------------------------------------------------------------+

+-------+--------------------+------------------+-----------------------------------------------------------+-------------------------------------------+
| 用户名	| 提交答卷时间		 | 【1】最坏 【2】最好	| 你有没有用过陆金所APP？有什么建议吗？							| 你最近有看过什么技术方面的书或文章吗？		|
+-------+--------------------+------------------+-----------------------------------------------------------+-------------------------------------------+
| 韩医徽	| 2018/8/31 15:38:09 | 			1		| 没有用过，对于理财app不是了解。想了解是否有类似花呗的借贷功能？	| 容器化；分布式环境的协调工具比如consul、etcd。	|
| 彦庆鑫	| 2018/8/31 15:38:50 | 			2		| 有，我希望有更多一年期的固收产品，另外陆金所到账时间太慢了。 	| 考过ai等方面的文章，技术人员，需要跟进了解。	|																		|
+-------+--------------------+------------------+-----------------------------------------------------------+-------------------------------------------+
'''


@logged(logging.getLogger("interview_generic"))

class InterviewGeneric(object):
	def __init__(self, QA_file):
		self.QA_file = QA_file
		self.candidates = []
		self.questions = []
		self.rules = []

	def data_load(self, data_file):
		data = pd.read_excel(data_file)
		return data

	def data_row_extract(self, data_in, selection):
		data_out = data_in.loc[selection, :]
		return data_out

	def data_column_extract(self, data_in, selection):
		data_out = data_in.loc[:, selection]
		return data_out

	def candidate_extract(self, data_in, criterion=True):
		candidates = []
		candidatemarks = []
		count = 0
		for candidate in data_in.index:
			if criterion == True:
				count += 1
				candidates.append(candidate)
				candidatemarks.append("p" + str(count))
		return candidates, candidatemarks

	def question_extract(self, data_in, criterion=True):
		questions = []
		questionmarks = []
		count = 0
		for question in data_in.columns:
			if criterion == True:
				count += 1
				questions.append(question)
				questionmarks.append("q" + str(count))
		return questions, questionmarks

	def data_rename(self, data_in, row, column):
		data_out = copy.deepcopy(data_in)
		data_out.index = row
		data_out.columns = column
		return data_out

	def recover_list_element(self, list_simple, list_complex, element):
		return list_complex[list_simple.index(element)]

	def data_iterate(data, cols=None): # 这相当于实现了pd.DataFrame.itertuples，但是效率更高。
		if cols is None:
			cols = data.columns.values.tolist()
			matrix = data.values.tolist()
		else:
			cols_indices = [data.columns.get_loc(c) for c in cols]
			matrix = data.values[:, cols_indices].tolist()
		tuple_named = namedtuple('tupling', cols)
		for line in iter(matrix):
			yield tuple_named(*line)

	def rate(self):
		pass