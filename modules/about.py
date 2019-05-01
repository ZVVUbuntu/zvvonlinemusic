"""About module"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class About(QWidget):
	"""About class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
		#add vbox main
		self.vbox_about = QVBoxLayout()
		self.setLayout(self.vbox_about)

		self.vbox_about.addStretch()
		#add image
		self.label_image = QLabel()
		self.label_image.setScaledContents(True)
		self.label_image.setPixmap(QPixmap(":/app_icon.png"))
		self.label_image.setFixedSize(100, 100)
		self.vbox_about.addWidget(self.label_image)
		self.vbox_about.setAlignment(self.label_image, Qt.AlignCenter)

		#add label name_program
		self.label_program = QLabel("ZVVOnlineMusic v.0.6")
		self.label_program.setAlignment(Qt.AlignCenter)
		self.label_program.setWordWrap(True)
		self.vbox_about.addWidget(self.label_program)
		#add label author
		self.label_author = QLabel(self.tr("Author: <b>Vyacheslav Zubik</b>. Ukraine, Kherson"))
		self.label_author.setAlignment(Qt.AlignCenter)
		self.label_author.setWordWrap(True)
		self.vbox_about.addWidget(self.label_author)
		#add blog
		self.label_blog = QLabel(self.tr("My blog: <a href = 'http://zvvubuntu.blogspot.com'>ZVVUbuntu</a>"))
		self.label_blog.setAlignment(Qt.AlignCenter)
		self.label_blog.setOpenExternalLinks(True)
		self.label_blog.setWordWrap(True)
		self.vbox_about.addWidget(self.label_blog)
		#add label email
		self.label_email = QLabel("Email:  ZVVUbuntu@gmail.com")
		self.label_email.setAlignment(Qt.AlignCenter)
		self.label_email.setTextInteractionFlags(Qt.TextSelectableByMouse)
		self.label_email.setWordWrap(True)
		self.vbox_about.addWidget(self.label_email)
		#add donate label
		self.label_donate = QLabel("My game - <a href = 'https://play.google.com/store/apps/details?id=com.ZVV.ZVVMinis'><b>ZVVMinis</b></a> - mini game pack.")
		self.label_donate.setOpenExternalLinks(True)
		self.label_donate.setWordWrap(True)
		self.label_donate.setAlignment(Qt.AlignCenter)
		self.vbox_about.addWidget(self.label_donate)
		
		self.vbox_about.addStretch()
