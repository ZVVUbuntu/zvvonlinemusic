#!/usr/bin/env python3
"""Main file"""
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from modules import widgets, paths, resources
if sys.platform.startswith('win'):
	import ctypes


class ZVVOnlineMusic(QMainWindow):
	"""Main class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()
			
	def create_widgets(self):
		"""Create central widget"""
		self.settings = QSettings(paths.config_path, QSettings.IniFormat)
		
		self.central_widget = widgets.Widgets()
		self.setCentralWidget(self.central_widget)
		
		self.setWindowIcon(QIcon(":/app_icon.png"))
		self.setWindowTitle("ZVVOnlineMusic")
		self.setFixedSize(450, 600)
		self.show()

##################################################################################

APP = QApplication(sys.argv)
if sys.platform.startswith('win'):
	MYAPPID = 'ZVVOnlineMusic'
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MYAPPID)
WIN = ZVVOnlineMusic()
sys.exit(APP.exec_())
