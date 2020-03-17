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
import concurrent.futures
import threading
import importlib
import time
import sip
import re

class MainArea(QWidget):
	def __init__(self):
		QWidget.__init__(self)

		self.Navigation_Urlbox = QLineEdit()
		self._Navigation_UrlButton = QPushButton("Go!")
		self._Navigation_UrlButton.clicked.connect(self.Navigation_UrlButton)

		NavigationLayout = QHBoxLayout()
		NavigationLayout.addWidget(QLabel("Url"))
		NavigationLayout.addWidget(self.Navigation_Urlbox)
		NavigationLayout.addWidget(self._Navigation_UrlButton)

		self.StatusLabel = QLabel()

		self.LoadLayout = QVBoxLayout()

		self.LoadWidget = QWidget()
		self.LoadWidget.setLayout(self.LoadLayout)

		TempLayout = QVBoxLayout()
		TempLayout.addWidget(self.LoadWidget)
		TempLayout.setContentsMargins(0, 0, 0, 0)
		TempLayout.setSpacing(0)
		TempLayout.addItem(QSpacerItem(0, 150, QSizePolicy.Minimum, QSizePolicy.Expanding))

		TempWidget = QWidget()
		TempWidget.setLayout(TempLayout)

		self.Load_ScrollArea = QScrollArea()
		self.Load_ScrollArea.setWidgetResizable(True)
		self.Load_ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.Load_ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.Load_ScrollArea.setWidget(TempWidget)

		MainLayout = QVBoxLayout()
		MainLayout.addLayout(NavigationLayout)
		MainLayout.addWidget(self.Load_ScrollArea)
		MainLayout.addWidget(self.StatusLabel)
		# -----------------------------------------------------------------------
		# ----- Preparing -------------------------------------------------------
		# -----------------------------------------------------------------------
		self.Count = 0
		self.ThreadPool = QThreadPool()

		self.setLayout(MainLayout)

	def DynamicUi(self, titleText="", pathText=""):
		DynamicUi_TitleLabel = QLabel(titleText)
		DynamicUi_TitleLabel.setObjectName("DynamicUi_TitleID" + str(self.Count))
		DynamicUi_StatusLabel = QLabel()
		DynamicUi_StatusLabel.setObjectName("DynamicUi_StatusID" + str(self.Count))
		DynamicUi_DirectoryLabel = QLabel("Path Directory: "+ os.path.dirname(os.path.realpath(__file__)) + str(chr(92))+"download"+str(chr(92)) + pathText)
		DynamicUi_ProgressBar = QProgressBar()
		DynamicUi_ProgressBar.setObjectName("DynamicUi_ProgressBarID" + str(self.Count))

		DynamicUi_Layout = QVBoxLayout()
		DynamicUi_Layout.addWidget(DynamicUi_TitleLabel)
		DynamicUi_Layout.addWidget(QLabel())
		DynamicUi_Layout.addWidget(DynamicUi_StatusLabel)
		DynamicUi_Layout.addWidget(DynamicUi_DirectoryLabel)
		DynamicUi_Layout.addWidget(DynamicUi_ProgressBar)

		DynamicUi_Widget = QWidget()
		DynamicUi_Widget.setLayout(DynamicUi_Layout)

		return DynamicUi_Widget

	def Navigation_UrlButton(self):
		if self.Navigation_Urlbox.text() != "":
			self.x = UrlThread(self.Navigation_Urlbox.text(), self.Count)
			self.x.status.connect(self.Navigation_UrlStatus)
			self.x.finished.connect(self.Navigation_UrlFinished)
			self.x.error.connect(self.Navigation_UrlError)
			self.x.start()

			self.Navigation_Urlbox.setText("")
			self._Navigation_UrlButton.setEnabled(False)

		else:
			QMessageBox.warning(self, "Error", "Empty!")

	def Navigation_UrlStatus(self, x):
		self.StatusLabel.setText(x)

	def Navigation_UrlError(self, x, y):
		if x is True:
			QMessageBox().warning(self, "Error", y)

			self.StatusLabel.setText("")
			self._Navigation_UrlButton.setEnabled(True)

	def Navigation_UrlFinished(self, x, y, z):
		self.StatusLabel.setText("")
		self._Navigation_UrlButton.setEnabled(True)
		self.LoadLayout.addWidget(self.DynamicUi(titleText=y["Title"], pathText=y["Title"]))
		self.Load_ScrollArea.verticalScrollBar().setValue(self.Load_ScrollArea.verticalScrollBar().maximum())

		self.Count += 1

		self.Thread = DownloadThread(y, z)
		self.Thread.signals.status.connect(self.Download_DynamicStatus)
		self.Thread.signals.finished.connect(self.Download_DynamicFinished)
		self.Thread.signals.error.connect(self.Download_DynamicError)

		self.ThreadPool.start(self.Thread)

	def Download_DynamicStatus(self, y):
		getStatus = self.LoadWidget.findChild(QLabel, "DynamicUi_StatusID" + str(y["ID"]))
		getStatus.setText("Status: " + y["Status"])

		getProgressbar = self.LoadWidget.findChild(QProgressBar, "DynamicUi_ProgressBarID" + str(y["ID"]))
		getProgressbar.setMaximum(y["Total"])
		getProgressbar.setValue(y["Current"])

		if y["Total"] == y["Current"] - 1:
			getProgressbar.setMaximum(100)
			getProgressbar.setValue(100)
		
	def Download_DynamicError(self, x, y):
		pass

	def Download_DynamicFinished(self, x):
		pass

class UrlThread(QThread):
	finished = pyqtSignal(bool, dict, int)
	error = pyqtSignal(bool, str)
	status = pyqtSignal(str)

	def __init__(self, x, y):
		QThread.__init__(self)

		self.getUrl = x
		self.getID = y

	def run(self):
		getPlugins = self.getUrl.split("/")[2].split(".")[1] if len(self.getUrl.split("/")[2].split(".")) == 3 else self.getUrl.split("/")[2].split(".")[0]

		if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "/plugins/" +getPlugins+ ".py") is True:
			try:
				self.status.emit("Fetching Data Information from [ " +self.getUrl+ " ]")

				getImport = importlib.import_module('.' +getPlugins, package='plugins')
				getFunction = getattr(getImport, getPlugins)
				getDictionary = getFunction.load(self, getUrl=self.getUrl)

				importlib.reload(getImport)

				self.finished.emit(True, getDictionary, self.getID)

			except Exception as e:
				self.error.emit(True, "[ " +getPlugins+ ".py ] =====>> " + str(e))

				print(e)

		else:
			self.error.emit(True, "There is no Plugins Name [" +getPlugins+  ".py] Exist!")

class DownloadObject(QObject):
	finished = pyqtSignal(bool)
	error = pyqtSignal(bool, str)
	status = pyqtSignal(dict)

class DownloadThread(QRunnable):
	def __init__(self, x, y, *args, **kwargs):
		QRunnable.__init__(self)

		self.Dictionary = x
		self.getID = y

		self.signals = DownloadObject()

	def run(self):
		for x in range(len(self.Dictionary['Page'])):
			r = requests.get(self.Dictionary['Page'][x], stream=True)
			title = self.Dictionary['Title']
			filename = self.Dictionary['Title'] +" "+ self.LeadingZeros_Format(x, len(str(len(self.Dictionary['Page'])))) +os.path.splitext(self.Dictionary['Page'][x])[1]

			if os.path.isdir(os.path.dirname(os.path.realpath(__file__)) +"/download/"+ title) is True:
				with open(os.path.dirname(os.path.realpath(__file__)) +"/download/"+ title +"/"+ filename, "wb+") as writeFile:
					for data in tqdm.tqdm(iterable=r.iter_content(chunk_size=1024), total=int(r.headers['content-length']) / 1024, unit="KB"):
						writeFile.write(data)

			else:
				os.makedirs("download/" + title)

				with open(os.path.dirname(os.path.realpath(__file__)) +"/download/"+ title +"/"+ filename, "wb+") as writeFile:
					for data in tqdm.tqdm(iterable=r.iter_content(chunk_size=1024), total=int(r.headers['content-length']) / 1024, unit="KB"):
						writeFile.write(data)

			self.signals.status.emit({
				"Current" : x,
				"Total" : len(self.Dictionary['Page']),
				"ID" : self.getID,
				"Status": "Downloading"
				})

		self.signals.status.emit({
				"Current" : 0,
				"Total" : len(self.Dictionary['Page']),
				"ID" : self.getID,
				"Status": "Finished"
			})

	def LeadingZeros_Format(self, num, size):
		s = str(num) + ""

		while len(s) < size:
			s = "0" + s

		return s

if __name__ == '__main__':
	App = QApplication(sys.argv)

	Config = MainArea()
	Config.resize(1000, 500)
	Config.setWindowTitle("Hacker-chan Version Alpha 1.1_02")
	Config.show()

	App.exec_()

# https://www.mangapanda.com/tanaka-kun-wa-itsumo-kedaruge/19