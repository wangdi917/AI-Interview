from __future__ import absolute_import, unicode_literals
import os, sys, argparse
import logging
from autologging import logged
import re
import warnings
# import threading
# import subprocess
from const import *
from configs.config import log_set_from_config, ConfigFactory
from log import log_to_ConsoleAndFile
from interview_JavaEng import InterviewJavaEng


warnings.filterwarnings("ignore")
# 这个文件中有print()！如果docker有要求那么可以去掉。


# SETTING_FILE = const.SETTING_FILE
current_path = os.path.dirname(os.getcwd()) + '/'
CONFIG = ConfigFactory(SETTING_FILE).load_config()
data_path = CONFIG.get("data", "data_path")
QA_record_general = current_path + data_path + CONFIG.get("data", "QA_record_general")
QA_type_general = CONFIG.get("data", "QA_type_general")
QA_record_technical = current_path + data_path + CONFIG.get("data", "QA_record_technical")
QA_type_technical = CONFIG.get("data", "QA_type_technical")
QA_record_simple = current_path + data_path + CONFIG.get("data", "QA_record_simple")
QA_type_simple = CONFIG.get("data", "QA_type_simple")


@logged(logging.getLogger("AI_Interview.main"))

def interviews():
	interviews._log.info("Java general questions are interviewed here:")
	class_JavaInterview = InterviewJavaEng(QA_record_simple, QA_type_simple)
	class_JavaInterview.execute()
	interviews._log.info("Java technical questions are interviewed here:")


@logged(logging.getLogger("AI_Interview.main"))

def main():
	# 加了一些并发功能在这里，以防未来在运行main()的同时还要运行其他功能。
	global threads
	global stop_threads
	stop_threads = False
	main._log.info("The main function starts here.")
	'''
	threads = [threading.Thread(target=interviews), threading.Thread(target=run_kafka), SimpleHTTPServer(CONFIG)]
	main._log.info("Started 3 threads: Interview, Kafka, and HTTP server for healthcheck.")
	for thread in threads:
		thread.start()
	time.sleep(1)
	'''
	interviews()
	'''
	for thread in threads:
		thread.join()
	main._log.info("Stopped 3 threads.")
	'''
	main._log.info("The main function stops here.")



if __name__ == "__main__":
	print ("\nThe entire program started now. May the force be with you!...\n")
	current_path = os.path.dirname(os.getcwd()) + '/'
	print ("The current path is {}.\n".format(current_path))
	log_target, log_level_console, log_level_file = log_set_from_config(current_path, SETTING_FILE)
	print ("The log file is {} with level={}&&{}.\n".format(log_target, log_level_console, log_level_file))

	log_to_ConsoleAndFile(log_target, log_level_console, log_level_file)
	try:
		sys.exit(main())
	except (KeyboardInterrupt, EOFError):
		print("\nThe entire program aborted due to keyboard interruption! Are you still there?\n")
		sys.exit(1)