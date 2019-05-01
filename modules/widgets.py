"""Widgets module"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from . import music_tab, about, equalizer, download


class Widgets(QWidget):
	"""Widgets class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(2, 2, 2, 2)
		self.setLayout(self.vbox_main)
	#tabber
		self.tabber = QTabWidget()
		self.tabber.tabBar().setIconSize(QSize(30, 30))
		self.vbox_main.addWidget(self.tabber)
		#music tab
		self.music_tab = music_tab.Music_tab(self)
		self.tabber.addTab(self.music_tab, QIcon(':/note.png'), "")
		#eq
		self.eq_tab = equalizer.Equalizer(self.music_tab)
		self.tabber.addTab(self.eq_tab, QIcon(":/eq_icon.png"), "")
		#download
		self.download_tab = download.Download(self)
		self.tabber.addTab(self.download_tab, QIcon(":/download.png"), "")
		#about
		self.about_win = about.About()
		self.tabber.addTab(self.about_win, QIcon(":/about_icon.png"), "")
		
