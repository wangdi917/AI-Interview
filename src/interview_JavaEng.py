from __future__ import absolute_import, unicode_literals, print_function, division
import os, sys, argparse
import logging
from autologging import logged
import numpy as np
import pandas as pd
import math
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from const import *
from interview_generic import InterviewGeneric
from approaches.match_regex import MatchRegularExpress
from approaches.match_dl import MatchDeepLearning


warnings.filterwarnings("ignore")


'''
+-------+---------------+-----------------------+-------------------------------------------------------------------------------------------+
| 用户名	|  账号 			| 面向对象的特性有哪些？	| 分布式缓存有哪些应用场景？																	|
+-------+---------------------------------------+-------------------------------------------------------------------------------------------+
| 张三	| zhangsan		| 我没有对象，怎么面向？	| 存储会话信息；为了缓解db压力从缓存查询提升性能；存储的都是一些不经常变动、对实时性要求不高的数据。	|
| 李四	| lisi			| 封装、继承、多态。		| 1.高性能 2.高qps场景 3.找工作面试场景 4.痛殴产品经理场景 5.和其他程序员聚会派对场景				|
+-------+---------------+-----------------------+-------------------------------------------------------------------------------------------+

+-------+--------------------+------------------------------+-------------------------------+
| 用户名	| 提交答卷时间		 | 我通常做【1】最坏【2】最好的打算	| 我业余时间喜欢【1】打游戏【2】泡妹子	|
+-------+--------------------+------------------------------+-------------------------------+
| 王五	| 2018/8/31 15:38:09 | 				1				|  				2				|
| 刘六	| 2018/8/31 15:38:50 | 				2				| 				1				|
+-------+--------------------+------------------------------+-------------------------------+
'''


@logged(logging.getLogger("interview_JavaEng"))

class InterviewJavaEng(InterviewGeneric):
	def __init__(self, QA_file, interview_type):
		self.interview_type = interview_type
		InterviewGeneric.__init__(self, QA_file) # 调用父类方法一
		# super(InterviewGeneric, self).__init__() # 调用父类方法二
		self.candidatemarks = []
		self.questionmarks = []
		self.__log.info("This class is sepcially for rating Java Engineer candidates.")
		self.__log.debug("Initialized the 'InterviewJavaEng' class using the 'InterviewGeneric' class.")


	def question_extract(self, data_in, interview_type):
		questions = []
		questionmarks = []
		count = 0
		for question in data_in.columns:
			if not '序号' in question and not '用户名' in question and not '提交答卷时间' in question and not '账号' in question and not '姓名' in question and not '部门' in question and not question.startswith('【'):
			# 原始表格中不全是面试问题，还有性格测试问题。所以，如果用是否有问号来区分并不可行，因为有些问题就是不以问号结尾。这样，只能姑且以hard coding来区分……
			# question[-1] == "?" or question[-2] == "?" or question[-1] == "？" or question[-2] == "？":
				count += 1
				questions.append(question)
				if interview_type == 'general':
					questionmarks.append("qg" + str(count))
				elif interview_type == 'technical':
					questionmarks.append("qt" + str(count))
				elif interview_type == 'characteristic':
					questionmarks.append("qc" + str(count))
				else:
					questionmarks.append("q" + str(count))
		# self.questions = questions
		# self.questionmarks = questionmarks
		return questions, questionmarks


	def prepare(self):
		data = self.data_load(self.QA_file)

		candidates, candidatemarks = self.candidate_extract(data) # 加载(Loading)
		self.__log.debug("The sampled candidates are {} as {}.".format(candidates[0:9], candidatemarks[0:9]))
		questions, questionmarks = self.question_extract(data, self.interview_type) # 重载(Overloading)
		self.__log.debug("The entire questions are {} as {}.".format(questions, questionmarks))

		# answers_to_question的横轴是原始的候选人索引、纵轴是提取出的问题。
		answers_to_question = self.data_column_extract(data, questions)
		# answers_to_questionmark的横轴是原始的候选人索引、纵轴是提取出的问题的标号。
		answers_to_questionmark = self.data_rename(answers_to_question, candidates, questionmarks)

		self.__log.debug("The data is {}.".format(answers_to_questionmark.iloc[[0],[0]])) # qg1 0 妹子多。
		self.__log.debug("The data is {}.".format(answers_to_questionmark.iloc[[0],[0]].columns)) # Index(['qg1'], dtype='object').
		self.__log.debug("The data is {}.".format(answers_to_questionmark.iloc[[0],[0]].index)) # Int64Index([0], dtype='int64').
		# self.__log.debug("All the data are {}.".format(answers_to_questionmark.head()))
		'''			qg1				qg2					qg9
			0	妹子多。				还没有。				暂时没有。
			1	钱多，人傻，速来。		有。					有做过相册日历抽彩票等等小程序。
			2	工资高。				用过。				哪有时间？！
			3	我没有其他offer。		有用过。太烂了！		自动登录小工具。
			4	女朋友也在这里。		女朋友用过。我没有。	基本都是九点半之后下班，没时间写小程序。 \n不过前段时间女友逼我写个抢红包的。
		'''
		return candidates, candidatemarks, questions, questionmarks, answers_to_questionmark


	def execute(self):
		candidates, candidatemarks, questions, questionmarks, answers_to_questionmark = self.prepare()
		class_re = MatchRegularExpress()
		class_dl = MatchDeepLearning()

		for index, row in answers_to_questionmark.iterrows():
			for quest in answers_to_questionmark.columns:
				# self.__log.debug("The point is {}.".format(row[quest]))
				pass

		for questionmark in questionmarks:
			if questionmark == 'qg11':
				class_dl.learning_summarize(answers_to_questionmark, questionmark, "book")
			elif questionmark == 'qg12':
				class_dl.learning_summarize(answers_to_questionmark, questionmark, "program")
			elif questionmark == 'qg1' or questionmark == 'qg2' or questionmark == 'qg3' or questionmark == 'qg4':
				score_for_questionX = class_re.rate_summarize(answers_to_questionmark, questionmark, questionmark, "max")
			else:
				match_percentage_for_questionX = class_re.callback_check(answers_to_questionmark, questionmark, questionmark)
