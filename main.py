from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 

from importlib import *
from requests_html import HTMLSession

import tqdm
import requests
import os
import io
import sys
import json
import tqdm
import concurrent.futures
import threading
import importlib
import time
import sip

class MainArea(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.Main_Urlbox = QLineEdit()
		Main_UrlButton = QPushButton("Download")
		Main_UrlButton.clicked.connect(self.Main_UrlButton)

		Group1 = QHBoxLayout()
		Group1.addWidget(self.Main_Urlbox)
		Group1.addWidget(Main_UrlButton)

		self.Main_Infobox = QTextEdit()
		self.Main_Infobox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.Main_Infobox.setReadOnly(True)
		# -----------------------------------------------------------------
		# ----- Preparing -------------------------------------------------
		# -----------------------------------------------------------------
		self.Loading = LoadingThread()
		self.Loading.loadingDot.connect(self.Main_LoadingRun)

		QMessageBox().warning(self, "Warning", "This App Version is Unstable!\nAny Error of this App, Please Report to the Official Developers Only!")

		MainLayout = QVBoxLayout()
		# MainLayout.setSpacing(0)
		# MainLayout.setContentsMargins(0,0,0,0)
		MainLayout.addWidget(QLabel("Url"))
		MainLayout.addLayout(Group1)
		MainLayout.addWidget(self.Main_Infobox)

		self.setLayout(MainLayout)

	def Main_UrlButton(self):
		if self.Main_Urlbox.text() != "":
			self.Main_Infobox.insertPlainText('Searching for ' +self.Main_Urlbox.text()+ '\nFetching Some Data ')

			self.x = Main_UrlThread(self.Main_Urlbox.text())
			self.x.info.connect(self.Main_UrlRun)
			self.x.error.connect(self.Main_ErrorRun)

			self.x.start()
			self.Loading.start()

			self.Main_Urlbox.setText('')

	def Main_UrlRun(self, x):
		self.Main_Infobox.insertPlainText(x)
		self.Loading.terminate()
		self.Main_Infobox.moveCursor(QTextCursor.End)

	def Main_LoadingRun(self, x):
		self.Main_Infobox.insertPlainText(x)

	def Main_ErrorRun(self, Error, DisplayError):
		if Error is True:
			QMessageBox().warning(self, "Error", DisplayError)
			self.Loading.terminate()
			self.Main_Infobox.moveCursor(QTextCursor.End)


class Main_UrlThread(QThread):
	info = pyqtSignal(str)
	finished = pyqtSignal()
	error = pyqtSignal(bool, str)

	def __init__(self, url):
		QThread.__init__(self)

		self.getUrl = url

	def run(self):
		splitUrl = self.getUrl.replace('www.', '').split('/', 25)
		Count = 0

		if os.path.isfile('plugins/' +os.path.splitext(splitUrl[2])[0]+ '.py') is True:
			getImport = importlib.import_module('.' +os.path.splitext(splitUrl[2])[0], package='plugins')
			getFunction = getattr(getImport, os.path.splitext(splitUrl[2])[0])
			getDictionary = getFunction.load(self, getUrl=self.getUrl)

			importlib.reload(getImport)
			
			self.info.emit('\n\nSources:\n' +str(getDictionary['Page']))
			self.info.emit('\n\nStart Downloading\n\n')

			for x in range(len(getDictionary['Page'])):
				with concurrent.futures.ThreadPoolExecutor() as Exe:
					self.info.emit(getDictionary['Title'] +" "+ self.LeadingZeros_Format(Count, len(str(len(getDictionary['Page'])))) +os.path.splitext(getDictionary['Page'][x])[1]+ " - Downloading\n")

					_Exe = Exe.submit(self.Download, getDictionary['Page'][x], getDictionary['Title'], getDictionary['Title'] +" "+ self.LeadingZeros_Format(Count, len(str(len(getDictionary['Page'])))) +os.path.splitext(getDictionary['Page'][x])[1])
					_Exe.result()

					self.info.emit(getDictionary['Title'] +" "+ self.LeadingZeros_Format(Count, len(str(len(getDictionary['Page'])))) +os.path.splitext(getDictionary['Page'][x])[1]+ " - Downloaded\n")

				Count += 1

			self.info.emit('\nDownload Complete!\n\n')

		else:
			self.error.emit(True, "There is no Plugins Name ["+os.path.splitext(splitUrl[2])[0]+ ".py] Exist!")

	def LeadingZeros_Format(self, num, size):
		s = str(num) + ""

		while len(s) < size:
			s = "0" + s

		return s

	def Download(self, http, title, filename):
		if os.path.isdir("download/" + title) is True:
			r = requests.get(http, stream=True)

			with open("download/"+ title +"/"+ filename, "wb+") as writeFile:
				for data in tqdm.tqdm(iterable=r.iter_content(chunk_size=1024), total=int(r.headers['content-length']) / 1024, unit="KB"):
					writeFile.write(data)

		else:
			os.makedirs("download/" + title)

			r = requests.get(http, stream=True)

			with open("download/"+ title +"/"+ filename, "wb+") as writeFile:
				for data in tqdm.tqdm(iterable=r.iter_content(chunk_size=1024), total=int(r.headers['content-length']) / 1024, unit="KB"):
					writeFile.write(data)


class LoadingThread(QThread):
	loadingDot = pyqtSignal(str)

	def run(self):
		while True:

			time.sleep(1)

			self.loadingDot.emit('.')

if __name__ == '__main__':
	App = QApplication(sys.argv)

	Config = MainArea()
	# Config.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
	# Config.setAttribute(Qt.WA_TranslucentBackground)
	Config.resize(1000, 500)
	Config.setWindowTitle("Hacker-chan Version Alpha 1.1_01")
	Config.show()

	App.exec_()