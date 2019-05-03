"""Download tab module"""
import os
import urllib.parse
import urllib.request
from urllib.request import Request, urlopen
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
							 QProgressBar, QFrame, QHBoxLayout, 
							 QPushButton, QScrollArea, QSizePolicy)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QCoreApplication, QDir, QSize, QThread
from . import zbutton


class Download(QScrollArea):
	"""Download Tab class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
		#widget_content
		self.widget_content = QWidget()
		self.setWidget(self.widget_content)
		
		#vbox_content
		self.vbox_content = QVBoxLayout()
		self.widget_content.setLayout(self.vbox_content)
		self.vbox_content.addStretch()
		
		###
		self.setWidgetResizable(True)
		self.setStyleSheet('QScrollArea{border:1px solid transparent}')

	def add_block(self, title, url):
		"""Add one block"""
		self.block = Block(self.parentWidget)
		self.vbox_content.insertWidget((self.vbox_content.count() - 1), self.block)
		self.block.download_file(title, url)

####################################################################

class Block(QFrame):
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
		self.FILE_PATH = None
		self.TITLE = None
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.setLayout(self.vbox_main)
		#hbox_title_close
		self.hbox_title_close = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_title_close)
		#label_title
		self.label_title = QLabel()
		self.label_title.setWordWrap(True)
		self.label_title.setStyleSheet('QLabel{color:blue; border:1px solid transparent;}')
		self.hbox_title_close.addWidget(self.label_title)
		#button_play
		self.button_play = zbutton.Zbutton()
		self.button_play.hide()
		self.button_play.set_info(icon=':/play.png')
		self.button_play.clicked.connect(self.press_button_play)
		self.hbox_title_close.addWidget(self.button_play)
		#button_close
		self.button_close = zbutton.Zbutton()
		self.button_close.set_info(icon=':/remove_icon.png')
		self.button_close.clicked.connect(self.press_button_close)
		self.hbox_title_close.addWidget(self.button_close)
		#progressbar_download
		self.progressbar_download = QProgressBar()
		self.progressbar_download.setRange(0, 0)
		self.progressbar_download.setStyleSheet('')
		self.vbox_main.addWidget(self.progressbar_download)
		
		###
		self.setMinimumHeight(40)
		self.setMaximumHeight(100)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.setStyleSheet('QFrame{border:1px solid silver; border-radius:5px;}')
		
	def get_normal_filename(self, file_name):
		"""Get normal filename"""
		file_name = file_name.replace(' ', '_')
		good_letters = 'abcdefghijklmnopqrstuvwxyz_абвгдеёжзийклмнопрстуфхцчшщъыьэюя_1234567890'
		normal_filename = ''.join(l for l in file_name if l.lower() in good_letters)
		return normal_filename
		
	def download_file(self, title, url):
		"""Download file"""
		self.label_title.setText(title)
		normal_title = self.get_normal_filename(title)
		self.download_one_item(normal_title, url)
		
	def download_one_item(self, title, url):
		"""Download one item"""
		music_folder = os.path.join(QDir.homePath(), 'Music')
		if not os.path.exists(music_folder):
			os.mkdir(music_folder)
		download_path = os.path.join(music_folder, '{}.mp3'.format(title))
		self.FILE_PATH = download_path
		self.TITLE = title
		self.new_thread = MyThread(url, download_path)
		self.new_thread.notifyProgress.connect(self.update_progress)
		self.new_thread.finished.connect(self.thread_finished)
		self.new_thread.start()
		
	def update_progress(self, value):
		"""Update download progress"""
		if not self.progressbar_download.maximum():
			self.progressbar_download.setRange(0, value)
		else:
			self.progressbar_download.setValue(value)
			
	def thread_finished(self):
		"""Thread finished"""
		self.progressbar_download.hide()
		self.progressbar_download.setValue(0)
		self.label_title.setStyleSheet('QLabel{color:grey; border:1px solid transparent;}')
		self.button_play.show()
		
	def press_button_close(self):
		"""Press button close"""
		self.hide()
		self.parent().layout().removeWidget(self)
		
	def press_button_play(self):
		"""Press button play"""
		if self.FILE_PATH:
			if os.path.exists(self.FILE_PATH):
				self.parentWidget.music_tab.player_play(self.TITLE, self.FILE_PATH)
		
#############################################################

class MyThread(QThread):
	"""MyThread class"""
	notifyProgress = QtCore.pyqtSignal(int)
	def __init__(self, url, output):
		super().__init__()
		self.output_file = output
		self.get_url = url

	def run(self):
		req = Request(self.get_url, headers={'User-Agent': 'Mozilla/5.0'})
		url_open = urlopen(req)
		meta = url_open.info()
		file_size = int(meta["Content-Length"])
		self.notifyProgress.emit(file_size)
		block_size = 4000
		value = 0
		with open(self.output_file, "wb") as file_open:
			while file_size > 0:
				file_open.write(url_open.read(block_size))
				file_size -= block_size
				value += block_size
				self.notifyProgress.emit(value)
		
