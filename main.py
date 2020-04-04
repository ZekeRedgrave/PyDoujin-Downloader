from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from importlib import *
from PIL import Image

import tqdm
import requests
import os
import sys
import json
import concurrent.futures
import importlib

import requests_html
import bs4
import selenium

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
		self.path = ""

		self.setLayout(MainLayout)

	def getSetting_JSON(self):
		SettingJSON = self.getJSON()
		getKey = []

		for key in SettingJSON:
			getKey.append(key)

		for i in getKey:
			if str.lower(i) is not "plugins":
				SettingJSON["plugins"] = {}

			elif str.lower(i) is not "download":
				SettingJSON["download"] = os.path.dirname(os.path.realpath(__file__))

		# if Path Directory of Download is Blank from Config File
		if SettingJSON["download"] == "":
			# if the Folder is Exist
			if os.path.isdir(os.path.dirname(os.path.realpath(__file__)) +"\\download") is True:
				SettingJSON["download"] = os.path.dirname(os.path.realpath(__file__))

			else:
				os.makedirs(os.path.dirname(os.path.realpath(__file__)) +"\\download")

				SettingJSON["download"] = os.path.dirname(os.path.realpath(__file__))

		else:
			if os.path.isdir(SettingJSON["download"] +"\\download") is False:
				os.makedirs(SettingJSON["download"] +"\\download")
		# Update
		SettingJSON.update()

		with open(os.path.dirname(os.path.realpath(__file__)) +"\\setting.json", "w+") as writeFile:
			writeFile.write(json.dumps(SettingJSON, indent=4))

		return SettingJSON

	def getJSON(self):
		# Preparing Variable
		SettingJSON = None
		# if setting.json exist
		if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) +"\\setting.json"):
			# get Data Information from setting.json
			with open(os.path.dirname(os.path.realpath(__file__)) + "\\setting.json", "r+") as readFile:
				SettingJSON = json.loads(readFile.read())

			return SettingJSON

		else:
			SettingJSON = {
				"plugins": {},
				"download": os.path.dirname(os.path.realpath(__file__))
			}

			if os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + "\\download") is False:
				os.makedirs("download")

			with open(os.path.dirname(os.path.realpath(__file__)) + "\\setting.json", "w+") as writeFile:
				writeFile.write(json.dumps(SettingJSON, indent=4))

		return SettingJSON

	def DynamicUi(self, titleText="", pathText=""):
		DynamicUi_TitleLabel = QLabel(titleText)
		DynamicUi_TitleLabel.setObjectName("DynamicUi_TitleID" + str(self.Count))
		DynamicUi_StatusLabel = QLabel()
		DynamicUi_StatusLabel.setObjectName("DynamicUi_StatusID" + str(self.Count))
		DynamicUi_DirectoryLabel = QLabel("Path Directory: "+ self.path +"\\"+ pathText)
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
		self.path = self.getSetting_JSON()["download"] + "\\download"

		self.StatusLabel.setText("")
		self._Navigation_UrlButton.setEnabled(True)
		self.LoadLayout.addWidget(self.DynamicUi(titleText=y["Title"], pathText=y["Title"]))
		self.Load_ScrollArea.verticalScrollBar().setValue(self.Load_ScrollArea.verticalScrollBar().maximum())

		self.Count += 1

		self.Thread = DownloadThread(y, z, self.path)
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
		
	def Download_DynamicError(self, title, say):
		QMessageBox().warning(self, "Error", "Title: " +title+ "\nDescription: " +say)

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
				# Reload External Python Script before using it
				importlib.reload(importlib.import_module('.' +getPlugins, package='plugins'))
				# Calling External Python Script
				getImport = importlib.import_module('.' +getPlugins, package='plugins')
				getDictionary = getImport.load(getUrl=self.getUrl)

				if self.CheckKeys(getDictionary) is True:
					self.finished.emit(True, getDictionary, self.getID)

				else:
					self.error.emit(True, "[ " +getPlugins+ ".py ] =====>> Either no Title, Page or Size Exist on Plugin's Script!\nPlease Complete the all requirements before you proceed to download!")

			except Exception as e:
				self.error.emit(True, "[ " +getPlugins+ ".py ] =====>> " + str(e))

		else:
			self.error.emit(True, "There is no Plugins Name [" +getPlugins+  ".py] Exist!")

	def CheckKeys(self, x={}):
		Gate = False

		for _x in x:
			if str(_x) is not "Title":
				Gate = False

			if str(_x) is not "Page":
				Gate = False

			if str(_x) is not "Size":
				Gate = False

			else:
				Gate = True

		return Gate

class DownloadObject(QObject):
	finished = pyqtSignal(bool)
	error = pyqtSignal(str, str)
	status = pyqtSignal(dict)

class DownloadThread(QRunnable):
	def __init__(self, x, y, z):
		QRunnable.__init__(self)

		self.Dictionary = x
		self.getID = y
		self.path = z
		self.Count = 0

		self.signals = DownloadObject()

	def run(self):
		# File Checking
		isBroken = []
		isExist = []
		Thread = []

		if os.path.isdir(self.path +"\\"+ self.Dictionary['Title']) is True:
			for x in range(len(self.Dictionary['Page'])):
				file = self.path +"\\" + self.Dictionary['Title'] +"\\"+ self.Dictionary['Title'] +" "+ self.LeadingZeros_Format(x, len(str(len(self.Dictionary['Page'])))) +os.path.splitext(self.Dictionary['Page'][x])[1]
				# if the file exist
				if os.path.isfile(file) is True:
					# if the file is equal the file size
					isExist.append(True)

					# try to open if the file is not broken
					try:
						if int(self.Dictionary['Size'][x]) == os.path.getsize(file):
							im = Image.open(file)
							isBroken.append(False)

						else:
							isBroken.append(True)

					except Exception as e:
							isBroken.append(True)

				else:
					isExist.append(False)
					isBroken.append(False)

				self.signals.status.emit({
					"Current" : x,
					"Total" : len(self.Dictionary['Page']),
					"ID" : self.getID,
					"Status": "File Checking"
				})

			self.signals.status.emit({
				"Current" : 0,
				"Total" : len(self.Dictionary['Page']),
				"ID" : self.getID,
				"Status": "Downloading"
			})

			for x in range(len(self.Dictionary['Page'])):
				r = requests.get(self.Dictionary['Page'][x], stream=True)
				file = self.path +"\\" + self.Dictionary['Title'] +"\\"+ self.Dictionary['Title'] +" "+ self.LeadingZeros_Format(x, len(str(len(self.Dictionary['Page'])))) +os.path.splitext(self.Dictionary['Page'][x])[1]
				folder = self.path +"\\"+ self.Dictionary['Title']
				# if the file is exist
				if isExist[x] is True:
					# if the file is broken
					if isBroken[x] is True:
						Thread.append(concurrent.futures.ThreadPoolExecutor().submit(self.Download, folder, file, r))

				else:
					Thread.append(concurrent.futures.ThreadPoolExecutor().submit(self.Download, folder, file, r))

			for x in concurrent.futures.as_completed(Thread):
				x.result()

		else:
			self.signals.status.emit({
				"Current" : 0,
				"Total" : len(self.Dictionary['Page']),
				"ID" : self.getID,
				"Status": "Downloading"
			})

			for x in range(len(self.Dictionary['Page'])):
				r = requests.get(self.Dictionary['Page'][x], stream=True)
				file = self.path +"\\" + self.Dictionary['Title'] +"\\"+ self.Dictionary['Title'] +" "+ self.LeadingZeros_Format(x, len(str(len(self.Dictionary['Page'])))) +os.path.splitext(self.Dictionary['Page'][x])[1]
				folder = self.path +"\\"+ self.Dictionary['Title']

				Thread.append(concurrent.futures.ThreadPoolExecutor().submit(self.Download, folder, file, r))
				
			for x in concurrent.futures.as_completed(Thread):
				x.result()

		self.signals.status.emit({
			"Current" : 0,
			"Total" : len(self.Dictionary['Page']),
			"ID" : self.getID,
			"Status": "Finished"
		})

	def Download(self, folder, file, r):
		try:
			if os.path.isdir(folder) is True:
				with open(file, "wb+") as writeFile:
					for data in tqdm.tqdm(iterable=r.iter_content(chunk_size=1024), total=int(r.headers['content-length']) / 1024, unit="KB", disable=True):
						writeFile.write(data)

			else:
				os.makedirs(folder)

				with open(file, "wb+") as writeFile:
					for data in tqdm.tqdm(iterable=r.iter_content(chunk_size=1024), total=int(r.headers['content-length']) / 1024, unit="KB", disable=True):
						writeFile.write(data)

			self.signals.status.emit({
				"Current" :self.Count,
				"Total" : len(self.Dictionary['Page']),
				"ID" : self.getID,
				"Status": "Downloading"
			})

			self.Count += 1

		except Exception as e:
			self.signals.error.emit(self.Dictionary["Title"], str(e))
			self.signals.status.emit({
				"Current" : 0,
				"Total" : len(self.Dictionary['Page']),
				"ID" : self.getID,
				"Status": "Failed"
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
	Config.setWindowTitle("Hacker-chan Version Alpha 1.2_01")
	Config.show()

	App.exec_()