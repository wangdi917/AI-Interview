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
# 因为整个项目的main.py需要在\interview-app\src\路径下运行，所以以上import可以实现。


warnings.filterwarnings("ignore")


@logged(logging.getLogger("approaches.match_regex"))

class MatchRegularExpress(object):
	def __init__(self):
		self.__log.info("The Regular Expression matching method is used for rating.")

		# SETTING_FILE = const.SETTING_FILE
		current_path = os.path.dirname(os.getcwd()) + '/'
		CONFIG = ConfigFactory(SETTING_FILE).load_config()
		callback_path = CONFIG.get("rule", "rule_path")
		callback_file = current_path + callback_path + CONFIG.get("rule", "callback_file")
		self.callback_file = callback_file
		rate_path = CONFIG.get("rule", "rule_path")
		rate_file = current_path + rate_path + CONFIG.get("rule", "rate_file")
		self.rate_file = rate_file
		# self.__log.debug("The Regular Expression rule file is located as {}.".format(self.rule_file))

	def load_rule(self, rule_file):
		with open(rule_file, encoding='utf-8') as load_f:
			dict_json = json.load(load_f)
		return dict_json


	def callback(self, answers_for_questionX, rules_for_questionX):
		# 计算所有预设关键词在所有已经入职的员工对同一问题的回答中出现的概率，类似于召回率。
		answers_for_questionX = answers_for_questionX.astype(str)
		matching_for_questionX = answers_for_questionX.copy()
		matching_for_questionX[:] = False
		# answers_for_questionX = [ 0				1					2				3				4
		# 							"陆金所妹子多", "钱多，人傻，速来", "陆金所工资高", "我没有其他offer", "女朋友也在这里"]

		for rule in rules_for_questionX:
			# rules = ["[0-9一两三]个?多?半?(小时)(.+分钟)?", "[0-9]+分钟", "浦东"]
			whether_match = answers_for_questionX.apply(lambda x: len(re.findall(rule, x))>0)
			matching_for_questionX += whether_match
		# answers_for_questionX是一个Series，所以apply和answers_for_questionX[answers_for_questionX]可以实现遍历answers_for_questionX，将原有的序列根据自身的T/F压缩成另一个序列。
		percentage_for_questionX = round(len(matching_for_questionX[matching_for_questionX>0])/len(matching_for_questionX) * 100, ndigits=2)
		# self.__log.debug("When doing callback, the matching result is\n{}\n".format(matching_for_questionX))
		# self.__log.debug("When doing callback, the matching percentage is {}/{} = {}.".format(len(matching_for_questionX[matching_for_questionX>0]), len(matching_for_questionX), percentage_for_questionX))
		return percentage_for_questionX


	def rate(self, answers_for_questionX, rules_for_questionX, score_scheme):
		# 计算所有已经入职的员工对同一问题的回答中匹配所有预设关键词的情况，根据预设权重打分。
		answers_for_questionX = answers_for_questionX.astype(str)
		score_for_questionX = answers_for_questionX.copy()
		score_for_questionX[:] = 0
		# answers_for_questionX = [ 0				1					2				3				4
		# 							"陆金所妹子多", "钱多，人傻，速来", "陆金所工资高", "我没有其他offer", "女朋友也在这里"]

		for level, rules in rules_for_questionX.items():
			# rules = {'Q':"为什么离职？", 'F1':"基本条件", 'W1':0.15, 'F2':"稳定性", 'W2':0.3, 'F3':"历史跳槽频率", 'W3':1, 'default':2, 'rule':'count', 'L5':["有","用过","忠实","粉丝","经常"], 'L3':["有时","偶尔","一些","一点"], 'L1':["没有","没用过","无"]},
			if level.startswith('L'):
				score_to_levelX = [0]*len(score_for_questionX)
				# score_to_levelX是对某个特定的rule比如'L5':["有","用过","忠实","粉丝","经常"]遍历["有","用过","忠实","粉丝","经常"]之后得到的分数。
				# score_for_questionX是对所有rules比如{'L1':[没有], 'L3':[偶尔], 'L5':[有]}遍历['L1','L3','L5']之后得到的分数。
				for rule in rules:
					# rules = ["有","用过","忠实","粉丝","经常"]
					whether_match = answers_for_questionX.apply(lambda x: int(len(re.findall(rule, x))>0) * int(level[-1]))
					self.__log.debug("Now trying to match answers\n'{}' to the key words '{}', the matching result is\n{}".format(answers_for_questionX, rule, whether_match))
					if score_scheme == "max":
						score_to_levelX = list(map(lambda x: max(x[0],x[1]), zip(score_to_levelX, whether_match)))
						self.__log.debug("Now updating the score due to the key words '{}' by choosing the max values between previous and present scores, the matching result is\n{}\n".format(rule, score_to_levelX))
					else:
						self.__log.error("Unrecognized scoring scheme '{}'!\n".format(score_scheme))
				self.__log.debug("\nHere all the key words in level '{}' rule {} have been iterated. The final score to this level and this rule is \n{}\n".format(level, rules, score_to_levelX))

				if score_scheme == "max":
					score_for_questionX = list(map(lambda x: max(x[0],x[1]), zip(score_for_questionX, score_to_levelX)))
					self.__log.debug("By summing the scores earned from level '{}' and all its previously iterated levels, the total score is\n{}\n".format(level, score_for_questionX))
				else:
					self.__log.error("Unrecognized scoring scheme '{}'!\n".format(score_scheme))
		return score_for_questionX


	def callback_check(self, answers, questionID, ruleID):
		dict_json = self.load_rule(self.callback_file)
		# self.__log.info("The callback rule file {} has been loaded.".format(self.callback_file))
		answers_for_questionX = answers[questionID]
		rules_for_questionX = dict_json[ruleID]
		percentage_for_questionX = self.callback(answers_for_questionX, rules_for_questionX)
		self.__log.info("For question '{}', examination rule '{}' is used for callback measurement.".format(questionID, ruleID))
		self.__log.debug("The match percentage among all the answers with respect to question '{}' and rule '{}' is {}%.".format(questionID, rules_for_questionX[0], percentage_for_questionX))
		return percentage_for_questionX


	def rate_summarize(self, answers, questionID, ruleID, score_scheme):
		dict_json = self.load_rule(self.rate_file)
		# self.__log.info("The rating rule file {} has been loaded.".format(self.rate_file))
		answers_for_questionX = answers[questionID]
		rules_for_questionX = dict_json[ruleID]
		score_for_questionX = self.rate(answers_for_questionX, rules_for_questionX, score_scheme)
		self.__log.info("For question '{}', regular expression rule '{}' is used for score rating.".format(questionID, ruleID))
		self.__log.debug("The total score with respect to question '{}' and rule '{}' is {}.".format(questionID, rules_for_questionX.keys(), score_for_questionX))
		return score_for_questionX