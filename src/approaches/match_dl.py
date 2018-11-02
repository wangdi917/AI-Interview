from __future__ import absolute_import, unicode_literals, print_function, division
import os, sys, argparse
import logging
from autologging import logged
import numpy as np
import pandas as pd
import re
import json
import warnings

from const import *
from configs.config import log_set_from_config, ConfigFactory
from approaches.NLP_methods import *
# 因为整个项目的main.py需要在\interview-app\src\路径下运行，所以以上import可以实现。


warnings.filterwarnings("ignore")


@logged(logging.getLogger("approaches.match_dl"))

class MatchDeepLearning(object):
	def __init__(self):
		self.__log.info("The Deep Learning matching method is used for rating.")
		self.nlp = China_No1()

	def book_count(self, nlp, sentence):
		doc = tokenize(nlp, sentence)
		doc = separate(nlp, sentence)
		booknames = 0
		for sent in doc.sents:
			for token in sent:
				if token.tag_.find("NN") != -1 or token.tag_.find("FW") != -1:
					# self.__log.debug("The token '{}' thanks to its attribute '{}' has been marked as a bookname.".format(token, token.tag_))
					booknames += 1
					break;
		self.__log.debug("Altogether {} booknames have been recorded.".format(booknames))
		return booknames

	def program_count(self, nlp, sentence):
		doc = tokenize(nlp, sentence)
		doc = separate(nlp, sentence)
		for sent in doc.sents:
			for token in sent:
				if token.tag_.find("NN") != -1 or token.tag_.find("FW") != -1:
					# self.__log.debug("The token '{}' thanks to its attribute '{}' has been marked as a programname.".format(token, token.tag_))
					self.__log.debug("A program name has been recorded.")
					return 1
		self.__log.debug("No program name has been recorded... which may be correct.")
		return 0

	'''
	"容器化；分布式环境的协调工具比如consul、etcd。", "book"
	"人月神话、block chain和AI VR最近很火。", "book"
	"做过，代码自动生成工具，根据数据库结构，自动生成前端到后端的单表CRUD。", "program"
	"基本上都是九点半之后下班，目前没时间写小程序。 不过前段时间写了一个idea的小插件。", "program"
	'''

	def learning_summarize(self, answers, questionID, learning_scheme):
		answers_for_questionX = answers[questionID]
		if learning_scheme == "book":
			score_for_questionX = answers_for_questionX.apply(lambda x: self.book_count(self.nlp, x))
			# score_for_questionX = self.book_count(self.nlp, answers_for_questionX)
		elif learning_scheme == "program":
			score_for_questionX = answers_for_questionX.apply(lambda x: self.program_count(self.nlp, x))
			# score_for_questionX = self.program_count(self.nlp, answers_for_questionX)
		else:
			self.__log.error("Unrecognized learning scheme '{}'!\n".format(learning_scheme))
		self.__log.info("For question '{}', learning scheme '{}' is used for score rating.".format(questionID, learning_scheme))
		self.__log.debug("The total score with respect to question '{}' is {}.".format(questionID, score_for_questionX))
		return score_for_questionX