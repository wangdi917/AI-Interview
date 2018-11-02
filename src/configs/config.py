import sys, argparse
import os.path
import logging
from autologging import logged
import warnings
import configparser as ConfigParser

sys.path.append("..")
from const import *

# warnings.filterwarnings("ignore")
# 这个文件中有print()！如果docker有要求那么可以去掉。


# SETTING_FILE = const.SETTING_FILE


def log_set_from_config(current_path, setting_file):
	config = ConfigParser.ConfigParser()
	try:
		config.read(setting_file)
		log_path = config.get('log', 'log_path')
		log_file = config.get('log', 'log_file')
		log_level_1 = config.get('log', 'log_level_console')
		log_level_2 = config.get('log', 'log_level_file')
		# log_target = os.path.dirname(os.getcwd()) + log_path + log_file + blank
		log_target = current_path + log_path + log_file
		print ("Nice. The setting file '{}' is valid.\n".format(setting_file))
	except Exception as e:
		print ("Error! The setting file '{}' is invalid! {}\n".format(setting_file, e))

	# repr()或%r方法以函数的形式对python机器描述一个对象，str()或%s方法以类型的形式对人描述一个对象。
	if log_level_1 == 'CRITICAL':
		log_level_console = logging.CRITICAL
	elif log_level_1 == 'ERROR':
		log_level_console = logging.ERROR
	elif log_level_1 == 'WARNING':
		log_level_console = logging.WARNING
	elif log_level_1 == 'INFO':
		log_level_console = logging.INFO
	else:
		log_level_console = logging.DEBUG

	if log_level_2 == 'CRITICAL':
		log_level_file = logging.CRITICAL
	elif log_level_2 == 'ERROR':
		log_level_file = logging.ERROR
	elif log_level_2 == 'WARNING':
		log_level_file = logging.WARNING
	elif log_level_2 == 'INFO':
		log_level_file = logging.INFO
	else:
		log_level_file = logging.DEBUG

	return log_target, log_level_console, log_level_file


class ConfigFactory(dict):
	# 输入一个字典，然后从任何外部文件中load configuration entries。
	config_file_defined = SETTING_FILE
	CONFIG = None

	def __init__(self, config_file_specified = None):
		if config_file_specified is not None:
			self.config_file_defined = config_file_specified
		else:
			pass
		# if self.config_file_defined.lower().endswith('.ini'):
		self.CONFIG = ConfigParser.ConfigParser()
		self.CONFIG.read(self.config_file_defined)

	def load_config(self):
		return self.CONFIG
	# CONFIG = ConfigFactory(SETTING_FILE).load_config()
	# self.Callback_key = CONFIG.get(JSON_KEYS, "Callback_key")
