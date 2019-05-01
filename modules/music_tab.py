"""Music_tab module"""
import sys
import os
import time
import random
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							 QLabel, QPushButton, QTableWidget, QTableWidgetItem,
							 QAbstractItemView, QHeaderView, QComboBox, QLineEdit)
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSize, QTimer
from . import vlc, styles, paths, controls, zbutton, parser


class Music_tab(QWidget):
	"""Music tab"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
		self.parser = parser.Parser(self)
		self.CURRENT_ITEM_NOW = None
		self.CURRENT_URL = None
		self.instance = vlc.Instance()
		self.PLAYER = self.instance.media_player_new()
		self.player_events = self.PLAYER.event_manager()
		self.player_events.event_attach(vlc.EventType.MediaPlayerLengthChanged, self.check_duration)
		self.player_events.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.check_position_state)
		
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(0, 2, 0, 0)
		self.vbox_main.setSpacing(1)
		self.setLayout(self.vbox_main)
		
	#hbox_tools
		self.hbox_tools = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_tools)
		#line
		self.line_search = QLineEdit()
		self.line_search.setFixedHeight(35)
		self.line_search.setPlaceholderText("search music (eg Mozart)")
		self.line_search.setClearButtonEnabled(True)
		self.line_search.returnPressed.connect(self.press_search)
		self.hbox_tools.addWidget(self.line_search)
		#combo_site
		self.model_site = QStandardItemModel()
		self.combo_site = QComboBox()
		self.combo_site.setModel(self.model_site)
		self.combo_site.setFixedSize(150, 35)
		self.combo_site.setFocusPolicy(Qt.NoFocus)
		self.hbox_tools.addWidget(self.combo_site)
		self.combo_site.addItem("Choose:")
		self.combo_site.addItem(QIcon(':/fav_icon.png'), "Favorites")
		for site in self.parser.LIST_SITES:
			item = SiteItem()
			item.set_info(site)
			self.model_site.appendRow(item)
		self.combo_site.activated.connect(self.choose_site)
		#button fav
		self.button_add_fav = zbutton.Zbutton()
		self.button_add_fav.setEnabled(False)
		self.button_add_fav.set_info(icon=':/fav_icon.png')
		self.button_add_fav.clicked.connect(self.press_add_favs)
		self.hbox_tools.addWidget(self.button_add_fav)
		#button_download
		self.button_download = zbutton.Zbutton()
		self.button_download.set_info(icon=':/download.png')
		self.button_download.clicked.connect(self.press_download)
		self.hbox_tools.addWidget(self.button_download)
		#button_remove_fav
		self.button_remove_fav = zbutton.Zbutton()
		self.button_remove_fav.hide()
		self.button_remove_fav.set_info(icon=':/remove_icon.png')
		self.button_remove_fav.clicked.connect(self.press_remove_fav)
		self.hbox_tools.addWidget(self.button_remove_fav)
		
	#label_title
		self.label_title = QLabel()
		self.label_title.setWordWrap(True)
		self.label_title.setAlignment(Qt.AlignCenter)
		self.label_title.setFixedHeight(40)
		self.label_title.setStyleSheet('QLabel{border:1px solid silver; color:brown; font-weight:bold; font-size:16px;}')
		self.vbox_main.addWidget(self.label_title)
		
	#table_widget
		self.table_widget = QTableWidget(0, 2)
		self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
		self.table_widget.setIconSize(QSize(24, 24))
		self.table_widget.verticalHeader().hide()
		self.table_widget.horizontalHeader().hide()
		self.table_widget.setShowGrid(True)
		self.table_widget.setWordWrap(False)
		self.table_widget.itemClicked.connect(self.check_in_fav_item)
		self.table_widget.itemDoubleClicked.connect(self.press_item)
		self.vbox_main.addWidget(self.table_widget)
		self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
		
		#controls_widget
		self.controls_widget = controls.Controls()
		self.vbox_main.addWidget(self.controls_widget)
		self.controls_widget.volume_slider.valueChanged.connect(self.volume_change)
		self.controls_widget.button_play.clicked.connect(self.press_play)
		self.controls_widget.button_pause.clicked.connect(self.press_pause)
		self.controls_widget.button_stop.clicked.connect(self.press_stop)
		self.controls_widget.button_next.clicked.connect(self.press_next_file)
		self.controls_widget.button_prev.clicked.connect(self.press_prev_file)
		self.controls_widget.button_minus_time.clicked.connect(self.press_minus_time)
		self.controls_widget.button_plus_time.clicked.connect(self.press_plus_time)
		
		#timer_check_end
		self.timer_check_end = QTimer()
		self.timer_check_end.setInterval(1000)
		self.timer_check_end.timeout.connect(self.play_end)
		self.timer_check_end.start()
		
		#AUTORUN
		self.volume_change(30)
#########################################################################################################

	def press_search(self):
		"""Press search"""
		text = self.line_search.text()
		if text:
			self.clear_all()
			current_index = self.combo_site.currentIndex()
			if current_index > 1:
				item = self.model_site.item(current_index)
				if item:
					url = item.URL
					self.parser.parse(text=text, url=url)
		
	def choose_site(self):
		"""Choose site"""
		self.clear_all()
		self.button_remove_fav.hide()
		current_index = self.combo_site.currentIndex()
		if current_index > 1:
			self.button_add_fav.setEnabled(True)
			item = self.model_site.item(current_index)
			if item:
				url = item.URL
				self.parser.parse(url=url)
		else:
			self.button_add_fav.setEnabled(False)
			if current_index == 1:
				self.set_favs()
				self.button_remove_fav.show()
				
	def set_favs(self):
		"""Set favs"""
		paths.BASE_CURSOR.execute('SELECT * FROM favs')
		found_items = paths.BASE_CURSOR.fetchall()
		for item in found_items:
			title, url = item[0], item[1]
			self.add_row(title, url)

	def add_row(self, text, url, duration=''):
		"""Add row"""
		#name
		fileNameItem = MyItem()
		fileNameItem.setText(text)
		fileNameItem.setIcon(QIcon(':/note.png'))
		fileNameItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
		fileNameItem.TITLE = text
		fileNameItem.URL = url
		#time
		timeItem = MyItem()
		timeItem.setText(duration)
		timeItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
		timeItem.setFlags(Qt.NoItemFlags)
		timeItem.TITLE = text
		timeItem.URL = url
		#set
		row = self.table_widget.rowCount()
		self.table_widget.insertRow(row)
		self.table_widget.setItem(row, 0, fileNameItem)
		self.table_widget.setItem(row, 1, timeItem)
		
	def press_item(self, item):
		"""Press double on item"""
		item.setIcon(QIcon(':/play_state.png'))
		if self.CURRENT_ITEM_NOW:
			if self.CURRENT_ITEM_NOW is not item:
				self.CURRENT_ITEM_NOW.setIcon(QIcon(':/note.png'))
		self.CURRENT_ITEM_NOW = item
		title = item.TITLE
		url = item.URL
		self.player_play(title, url)
		
	def check_in_fav_item(self):
		"""Select item"""
		if self.combo_site.currentIndex() > 1:
			current_item = self.table_widget.currentItem()
			if current_item:
				check_params = [current_item.TITLE,]
				paths.BASE_CURSOR.execute('SELECT * FROM favs WHERE name=?', check_params)
				found = paths.BASE_CURSOR.fetchone()
				if found:
					self.button_add_fav.setEnabled(False)
				else:
					self.button_add_fav.setEnabled(True)
		
	def press_add_favs(self):
		"""Press add to favs"""
		current_item = self.table_widget.currentItem()
		if current_item:
			insert_params = [current_item.TITLE, current_item.URL]
			paths.BASE_CURSOR.execute('SELECT * FROM favs WHERE name=? AND url=?', insert_params)
			found = paths.BASE_CURSOR.fetchone()
			if not found:
				paths.BASE_CURSOR.execute('INSERT INTO favs VALUES(?,?)', insert_params)
				paths.BASE_CONNECTION.commit()
				
	def press_remove_fav(self):
		"""Press remove fav"""
		current_item = self.table_widget.currentItem()
		if current_item:
			remove_params = [current_item.TITLE, current_item.URL]
			paths.BASE_CURSOR.execute('DELETE FROM favs WHERE name=? AND url=?', remove_params)
			paths.BASE_CONNECTION.commit()
			self.table_widget.removeRow(current_item.row())
		
	def press_download(self):
		"""Press download"""
		current_item = self.table_widget.currentItem()
		if current_item:
			title = current_item.TITLE
			url = current_item.URL
			self.parentWidget.download_tab.add_block(title, url)
		
	def clear_all(self):
		"""Clear all"""
		self.table_widget.setRowCount(0)
		self.CURRENT_ITEM_NOW = None
		
	def clear_info(self):
		"""Clar info"""
		self.controls_widget.clear_info()
		self.label_title.clear()
		self.CURRENT_ITEM_NOW.setIcon(QIcon(':/note.png'))
		self.CURRENT_ITEM_NOW = None
		
######################################PLAYER#############################################################

	def volume_change(self, value):
		"""Volume change"""
		volume = "Volume: {0}".format(str(value))
		self.PLAYER.audio_set_volume(value)
		self.controls_widget.label_volume.setText(volume)
		self.controls_widget.volume_slider.setValue(value)

	def press_play(self):
		"""Press play"""
		self.PLAYER.play()

	def press_pause(self):
		"""Press pause"""
		self.PLAYER.pause()
		
	def press_stop(self):
		"""Press stop"""
		self.PLAYER.stop()
		self.clear_info()
		
	def player_play(self, title, url):
		"""Player play"""
		self.label_title.setText(title)
		self.CURRENT_URL = url
		self.media = self.instance.media_new(url)
		self.PLAYER.set_media(self.media)
		self.PLAYER.play()

######################################TIME CONTROL#########################################################

	def check_duration(self, event):
		"""Check duration"""
		last_time = self.PLAYER.get_media().get_duration()
		if last_time:
			self.controls_widget.time_slider.setRange(0, last_time)
			last_time = time.strftime('%H:%M:%S', time.gmtime(last_time/1000.0))
			self.controls_widget.label_pos_last.setText(str(last_time))
		
	def check_position_state(self, event):
		"""Check position state"""
		value = self.PLAYER.get_position()
		value = value * self.controls_widget.time_slider.maximum()
		current_time = int(value)
		self.move_time(current_time)
		
	def show_move(self, value):
		"""Show move position"""
		move_time = time.strftime('%H:%M:%S', time.gmtime(value/1000.0))
		self.controls_widget.label_move_time.setText(move_time)
		
	def move_time(self, position):
		"""Position"""
		self.controls_widget.time_slider.setValue(position)
		current_label_time = time.strftime('%H:%M:%S', time.gmtime(position/1000.0))
		self.controls_widget.label_pos_current.setText(str(current_label_time))
			
	def set_pos(self, position):
		"""Set position"""
		max_value = self.controls_widget.time_slider.maximum()
		set_time = ((position * 100) / max_value) / 100
		self.PLAYER.set_position(set_time)
		
	def play_end(self):
		"""Play end"""
		if self.PLAYER.get_state() == vlc.State.Ended:
			self.choose_play_mode()
			
	def press_minus_time(self):
		"""Press minus time"""
		current_pos = self.controls_widget.time_slider.value()
		if current_pos:
			current_pos -= 10000
			self.set_pos(current_pos)
		
	def press_plus_time(self):
		"""Press plus time"""
		current_pos = self.controls_widget.time_slider.value()
		if current_pos:
			current_pos += 15000
			self.set_pos(current_pos)
		
#####################################PLAY ORDER##################################################

	def choose_play_mode(self):
		"""Choose mode"""
		if self.table_widget.rowCount() > 0:
			current_mode = self.controls_widget.combo_playmodes.currentText().lower()
			if current_mode == "replay":
				self.player_play(self.label_info.text(), self.CURRENT_URL)
			if current_mode in ["next", "shuffle"]:
				self.press_next_file()

	def press_prev_file(self):
		"""Press prev file"""
		max_files = self.table_widget.rowCount()
		if max_files:
			current_item = self.table_widget.currentItem()
			if current_item:
				current_row = current_item.row()
				if self.controls_widget.combo_playmodes.currentText().lower() == "shuffle":
					current_row = random.randrange(0, (max_files-1))
				else:
					current_row -= 1
				if current_row < 0:
					current_row = 0
				self.next_file(current_row)

	def press_next_file(self):
		"""Press next file"""
		max_files = self.table_widget.rowCount()
		if max_files > 0:
			current_item = self.table_widget.currentItem()
			if current_item:
				current_row = current_item.row()
				if self.controls_widget.combo_playmodes.currentText().lower() == "shuffle":
					current_row = random.randrange(0, (max_files-1))
				else:
					current_row += 1
				self.next_file(current_row)
			
	def next_file(self, index):
		"""Play Next file"""
		if index >= 0 and index < self.table_widget.rowCount():
			next_item = self.table_widget.item(index, 0)
			self.table_widget.setCurrentItem(next_item)
			self.press_item(next_item)
			
#####################################################################################################

class MyItem(QTableWidgetItem):
	"""My Item class"""
	def __init__(self):
		super().__init__()
		self.TITLE = None
		self.URL = None
		self.setFlags(self.flags() ^ Qt.ItemIsEditable)
		
class SiteItem(QStandardItem):
	"""Site item"""
	def __init__(self):
		super().__init__()
		self.TITLE = None
		self.URL = None
		self.setFlags(self.flags() ^ Qt.ItemIsEditable)
		self.setIcon(QIcon(":/url.png"))
		
	def set_info(self, url):
		"""Set info"""
		title = os.path.split(url)[-1]
		self.setText(title)
		self.TITLE = title
		self.URL = url
