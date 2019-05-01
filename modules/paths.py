"""Pathes module"""
import os
import sys
import sqlite3
import shutil
from PyQt5.QtCore import Qt, QDir, QStandardPaths

if sys.platform.startswith('linux'):
	system_path = os.path.join(os.getenv("HOME"), ".config")
	if not os.path.exists(system_path):
		os.mkdir(system_path)
	path_program = os.path.join(system_path, "ZVVOnlineMusic")
	if not os.path.exists(path_program):
		os.mkdir(path_program)
	config_path = os.path.join(path_program, "config.ini")
	if not os.path.exists(config_path):
		src_path = os.path.join(os.getcwd(), "config.ini")
		shutil.copy(src_path, path_program)
	base_path = os.path.join(path_program, "favs.db")
	if not os.path.exists(base_path):
		src_path = os.path.join(os.getcwd(), "favs.db")
		shutil.copy(src_path, path_program)
	record_path = QStandardPaths.writableLocation(QStandardPaths.MusicLocation)

if sys.platform.startswith('win'):
	path_program = os.getcwd()
	config_path = os.path.join(path_program, "config.ini")
	base_path =  os.path.join(path_program, "favs.db")
	record_path = QStandardPaths.writableLocation(QStandardPaths.MusicLocation)

BASE_CONNECTION = sqlite3.connect(base_path)
BASE_CURSOR = BASE_CONNECTION.cursor()
