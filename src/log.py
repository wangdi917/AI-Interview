import os, sys, argparse
import logging
from autologging import logged
import warnings

# warnings.filterwarnings("ignore")


def log_to_ConsoleAndFile(log_file, log_level_console, log_level_file):
	logging.basicConfig(level=log_level_file, format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s", 
					datefmt='%Y-%b%d-%H:%M:%S', filename=log_file, filemode='w')
	console = logging.StreamHandler()
	console.setLevel(log_level_console)
	formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)