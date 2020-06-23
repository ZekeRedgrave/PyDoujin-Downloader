from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import requests
import os
import sys
import json
import concurrent.futures
import importlib
import sqlite3
import datetime
import functools

import tqdm
import bs4
import selenium

class MainWidget(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		# -----------------------------------------------------------------------
		# ----- Main ------------------------------------------------------------
		# -----------------------------------------------------------------------
		self.MainNavigation_Downloadbox = QLineEdit()
		MainNavigation_DownloadButton = QPushButton("Download")
		MainNavigation_DownloadButton.clicked.connect(self.DownloadButton)
		MainNavigation_SettingButton = QPushButton("Setting")

		MainNavigation_Layout = QHBoxLayout()
		MainNavigation_Layout.addWidget(self.MainNavigation_Downloadbox)
		MainNavigation_Layout.addWidget(MainNavigation_DownloadButton)
		MainNavigation_Layout.addWidget(MainNavigation_SettingButton)

		self.MainContainer_ListWidget = QListWidget()
		self.MainContainer_ListWidget.setSortingEnabled(True)

		MainLayout = QVBoxLayout()
		MainLayout.addLayout(MainNavigation_Layout)
		MainLayout.addWidget(self.MainContainer_ListWidget)
		# -----------------------------------------------------------------------
		# ----- Preparing -------------------------------------------------------
		# -----------------------------------------------------------------------
		self.ThreadPool = QThreadPool()
		self.LocalSQL = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\app.db")
		self.Count = 0
		self.ListWidth = 0
		self.ListHeight = 0
		
		self.setLayout(MainLayout)

	def DownloadButton(self):
		if self.MainNavigation_Downloadbox.text() != "":
			self.PreparingThread = DownloadThread(self.Count, self.MainNavigation_Downloadbox.text())
			self.PreparingThread.Signals.status.connect(self.DownloadStatus)
			self.PreparingThread.Signals.error.connect(self.DownloadError)
			self.ThreadPool.start(self.PreparingThread)

			self.MainContainer_RectangleList(self.Count, self.MainNavigation_Downloadbox.text())

			self.MainNavigation_Downloadbox.setText("")
			self.Count += 1

	# Others
	def DownloadError(self, json):
		if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "\\log.txt") is True: 
			x = open(os.path.dirname(os.path.realpath(__file__)) + "\\log.txt", "r+").read()
				
			open(os.path.dirname(os.path.realpath(__file__)) + "\\log.txt", "w+").write(x+ "\n" +json["ErrorDisplay"])
		else: open(os.path.dirname(os.path.realpath(__file__)) + "\\log.txt", "w+").write(json["ErrorDisplay"])

		Alert = QMessageBox()
		Alert.setWindowTitle("Error")
		Alert.setText(json["ErrorDisplay"])
		Alert.show()

	def DownloadStatus(self, json):
		CoverImage = self.findChild(QLabel, "CoverPage_ID"+ str(json["ID"]))
		TitleLabel = self.findChild(QLabel, "TitleLabel_ID"+ str(json["ID"]))
		StatusLabel = self.findChild(QLabel, "StatusLabel_ID"+ str(json["ID"]))
		PageLabel = self.findChild(QLabel, "PageLabel_ID"+ str(json["ID"]))
		SizeLabel = self.findChild(QLabel, "SizeLabel_ID"+ str(json["ID"]))
		ProgressBar = self.findChild(QProgressBar, "ProgressBar_ID"+ str(json["ID"]))
		DirectoryButton = self.findChild(QPushButton, "DirectoryButton_ID"+ str(json["ID"]))

		if json["isError"] is True:
			if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "\\log.txt") is True: 
				x = open(os.path.dirname(os.path.realpath(__file__)) + "\\log.txt", "r+").read()
				
				open(os.path.dirname(os.path.realpath(__file__)) + "\\log.txt", "w+").write(x+ "\n" +json["ErrorDisplay"])
			else: open(os.path.dirname(os.path.realpath(__file__)) + "\\log.txt", "w+").write(json["ErrorDisplay"])

			TitleLabel.setText("Error Detected! Check the Logs for Full Information!")
			StatusLabel.setText("")
			PageLabel.setText("")
		
		else:
			if json["Cover"] != "":
				getImage = QPixmap(json["Cover"])
				getImage = getImage.scaledToHeight(self.ListWidth)

				CoverImage.setPixmap(getImage)
				# CoverImage.setScaledContents(True)
				# CoverImage.setAlignment(Qt.AlignCenter)
				
			if json["Title"] != "": TitleLabel.setText(json["Title"])
			if json["Directory"] != "": DirectoryButton.clicked.connect(functools.partial(self.DirectoryButton, json["Directory"]))
			if json["Status"] != "": StatusLabel.setText(json["Status"])
			if json["CurrentSize"] == json["TotalSize"]:
				StatusLabel.setText("Done")
				PageLabel.setText("Page " +str(json["TotalPage"])+ " to Page " +str(json["TotalPage"]))
				ProgressBar.setMaximum(json["TotalSize"])
				ProgressBar.setValue(json["TotalSize"])

			else:
				SizeLabel.setText(str(json["CurrentSize"])+ "B to " +str(json["TotalSize"])+ "B")
				PageLabel.setText("Page " +str(json["CurrentPage"])+ " to Page " +str(json["TotalPage"]))
				ProgressBar.setMaximum(json["TotalSize"])
				ProgressBar.setValue(json["CurrentSize"])

	# https://www.mangapanda.com/tanaka-kun-wa-itsumo-kedaruge/32

	def MainContainer_RectangleList(self, FetchID, FetchUrl):
		CoverPage = QLabel()
		CoverPage.setContentsMargins(0, 0, 10, 0)
		CoverPage.setObjectName("CoverPage_ID"+ str(FetchID))

		TitleLabel = QLabel("Fetching Data [ "+ FetchUrl +" ]")
		TitleLabel.setWordWrap(True)
		TitleLabel.setObjectName("TitleLabel_ID"+ str(FetchID))
		StatusLabel = QLabel()
		StatusLabel.setObjectName("StatusLabel_ID"+ str(FetchID))
		StatusLabel.setContentsMargins(0, 80 ,0 ,0)
		PageLabel = QLabel()
		PageLabel.setObjectName("PageLabel_ID"+ str(FetchID))
		SizeLabel = QLabel()
		SizeLabel.setObjectName("SizeLabel_ID"+ str(FetchID))

		ProgressBar = QProgressBar()
		ProgressBar.setObjectName("ProgressBar_ID"+ str(FetchID))
		ProgressBar.setTextVisible(False)
		DirectoryButton = QPushButton("Directory")
		DirectoryButton.setObjectName("DirectoryButton_ID"+ str(FetchID))
		# RemoveButton = QPushButton("Remove")
		RectangleList_FooterLayout = QHBoxLayout()
		RectangleList_FooterLayout.addWidget(ProgressBar)
		RectangleList_FooterLayout.addWidget(DirectoryButton)
		# RectangleList_FooterLayout.addWidget(RemoveButton)

		RectangleList_RightLayout = QVBoxLayout()
		RectangleList_RightLayout.setSpacing(0)
		RectangleList_RightLayout.setContentsMargins(0, 0, 0, 0)
		RectangleList_RightLayout.addWidget(TitleLabel)
		RectangleList_RightLayout.addWidget(StatusLabel)
		RectangleList_RightLayout.addWidget(PageLabel)
		RectangleList_RightLayout.addWidget(SizeLabel)
		RectangleList_RightLayout.addLayout(RectangleList_FooterLayout)

		RectangleList_Layout = QHBoxLayout()
		RectangleList_Layout.setSpacing(0)
		RectangleList_Layout.setContentsMargins(10, 10, 10, 10)
		RectangleList_Layout.addWidget(CoverPage)
		RectangleList_Layout.addLayout(RectangleList_RightLayout)

		RectangleList_Widget = QWidget()
		RectangleList_Widget.setObjectName(str(FetchID))
		RectangleList_Widget.setLayout(RectangleList_Layout)

		Item = QListWidgetItem()
		Item.setSizeHint(RectangleList_Widget.sizeHint())

		Size = QSize(Item.sizeHint())

		Test = QPixmap("cover.png")
		Test = Test.scaledToHeight(Size.height())
		CoverPage.setPixmap(Test)

		self.ListWidth = Size.width()
		self.ListHeight = Size.height()
		self.MainContainer_ListWidget.addItem(Item)
		self.MainContainer_ListWidget.setItemWidget(Item, RectangleList_Widget)

	def DirectoryButton(self, Directory):
		os.startfile(Directory)

class DownloadObject(QObject):
	finished = pyqtSignal(dict)
	status = pyqtSignal(dict)
	error = pyqtSignal(dict)

class DownloadThread(QRunnable):
	def __init__(self, FetchID, FetchUrl):
		QRunnable.__init__(self)

		self.FetchID = FetchID
		self.FetchUrl = FetchUrl
		self.FetchJSON = {
			"FetchUrl": FetchUrl,
			"FetchTitle": "",
			"FetchCode": "",
			"FetchAA": "",
			"FetchTag": {},
			"FetchCover": "",
			"FetchSrc": [],
			"FetchSize": [],
			"DateRegister" : datetime.datetime.now().strftime("%Y")+ "年" +datetime.datetime.now().strftime("%m") +"月"+ datetime.datetime.now().strftime("%d") +"日",
			"TimeRegister" : datetime.datetime.now().strftime("%H")+ "時" +datetime.datetime.now().strftime("%M") +"分"+ datetime.datetime.now().strftime("%S") +"秒"
		}
		self.FetchTitle = ""
		self.PageCount = 0
		self.PageTotal = 0
		self.CurrentSize = 0
		self.TotalSize = 0
		self.LocalSQL = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\app.db")
		self.Signals = DownloadObject()

	def run(self):	
		try:
			getPlugins = self.FetchUrl.split("/")[2].split(".")[1] if len(self.FetchUrl.split("/")[2].split(".")) == 3 else self.FetchUrl.split("/")[2].split(".")[0]
			if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "/plugins/" +getPlugins+ ".py") is True:
				# Reload External Python Script before using it
				importlib.reload(importlib.import_module('.' +getPlugins, package='plugins'))
				# Calling External Python Script
				getImport = importlib.import_module('.' +getPlugins, package='plugins')
				getDictionary = getImport.load(getUrl=self.FetchUrl)

				print(getDictionary)

				thread = []
				count = 0

				for x in getDictionary["Size"]: self.TotalSize += int(x)

				self.FetchTitle = getDictionary["Title"]
				self.PageTotal = len(getDictionary["Src"])
				self.Signals.status.emit({
					"isError": False,
					"ID": self.FetchID,
					"Title": getDictionary["Title"],
					"Cover": "",
					"Status": "Preparing",
					"Directory": "",
					"CurrentSize": self.CurrentSize,
					"TotalSize": self.TotalSize,
					"CurrentPage": self.PageCount,	
					"TotalPage": self.PageTotal
				})
					
				r = requests.get(getDictionary["Cover"], stream=True)

				with open(os.path.dirname(os.path.realpath(__file__))+ "\\download\\" + getDictionary["Title"]+ os.path.splitext(getDictionary["Cover"])[1], "wb+") as writeFile:
					for data in tqdm.tqdm(iterable=r.iter_content(chunk_size=1024), total=int(r.headers["content-length"]) / 1024, unit="KB"):
						writeFile.write(data)

				self.Signals.status.emit({
					"isError": False,
					"ID": self.FetchID,
					"Title": "",
					"Cover": os.path.dirname(os.path.realpath(__file__))+ "\\download\\" + getDictionary["Title"]+ os.path.splitext(getDictionary["Cover"])[1],
					"Status": "",
					"Directory": "",
					"CurrentSize": self.CurrentSize,
					"TotalSize": self.TotalSize,
					"CurrentPage": self.PageCount,
					"TotalPage": self.PageTotal
				})

				for x in getDictionary["Src"]:
					thread.append(concurrent.futures.ThreadPoolExecutor().submit(self.Download, os.path.dirname(os.path.realpath(__file__))+ "\\download\\" + getDictionary["Title"], os.path.dirname(os.path.realpath(__file__))+ "\\download\\" + getDictionary["Title"]+ "\\" +getDictionary["Title"]+ " " +self.LeadingZeros_Format(count, len(str(len(getDictionary["Src"]))) )+ os.path.splitext(x)[1], x))
					count += 1

				self.Signals.status.emit({
					"isError": False,
					"ID": self.FetchID,
					"Title": "",
					"Cover": "",
					"Status": "Downloading",
					"Directory": os.path.dirname(os.path.realpath(__file__))+ "\\download\\" + getDictionary["Title"],
					"CurrentSize": self.CurrentSize,
					"TotalSize": self.TotalSize,
					"CurrentPage": self.PageCount,
					"TotalPage": self.PageTotal
				})

				for x in concurrent.futures.as_completed(thread):
					x.result()

			else:
				self.Signals.error.emit({
					"isError": True,
					"ID": self.FetchID,
					"ErrorDisplay": self.DateTime() +" => There is no Plugin Name [" +getPlugins+  ".py] Exist!"
				})

		except Exception as e:
			self.Signals.status.emit({
				"isError": True,
				"ID": self.FetchID,
				"ErrorDisplay": self.DateTime() +" => " + str(e)
			})
		

	def Download(self, folder, file, src):
		try:
			if os.path.isdir(folder) is True:
				r = requests.get(src, stream=True)

				with open(file, "wb+") as writeFile:
					for data in tqdm.tqdm(iterable=r.iter_content(chunk_size=1024), total=int(r.headers["content-length"]) / 1024, unit="KB"):
						x = data

						writeFile.write(x)

						self.CurrentSize += len(bytes(x))
						self.Signals.status.emit({
							"isError": False,
							"ID": self.FetchID,
							"Title": self.FetchTitle,
							"Cover": "",
							"Status": "Downloading",
							"Directory": "",
							"CurrentSize": self.CurrentSize,
							"TotalSize": self.TotalSize,
							"CurrentPage": self.PageCount,
							"TotalPage": self.PageTotal
						})

				self.Signals.status.emit({
					"isError": False,
					"ID": self.FetchID,
					"Title": self.FetchTitle,
					"Cover": "",
					"Status": "Downloading",
					"Directory": "",
					"CurrentSize": self.CurrentSize,
					"TotalSize": self.TotalSize,
					"CurrentPage": self.PageCount,
					"TotalPage": self.PageTotal
				})
				self.PageCount += 1

			else:
				os.makedirs(folder)

				self.Download(folder, file, src)

		except Exception as e:
			self.Signals.status.emit({
				"isError": True,
				"ID": self.FetchID,
				"ErrorDisplay": self.DateTime() +" => " + str(e)
			})
			self.Download(folder, file, src)

	def DateTime(self):
		Date = datetime.datetime.now().strftime("%Y")+ ":" +datetime.datetime.now().strftime("%m") +":"+ datetime.datetime.now().strftime("%d") +":"
		Time = datetime.datetime.now().strftime("%H")+ ":" +datetime.datetime.now().strftime("%M") +":"+ datetime.datetime.now().strftime("%S") +":"

		return Date +" "+ Time

	def LeadingZeros_Format(self, num, size):
		s = str(num) + ""

		while len(s) < size:
			s = "0" + s

		return s 

if __name__ == '__main__':
	sys.path.append(os.path.dirname(os.path.realpath(__file__)))

	if os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + "plugins") is False:
		os.makedirs(os.path.dirname(os.path.realpath(__file__)) + "plugins")

	LocalSQL = None

	if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "\\app.db") is False:
		LocalSQL = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\app.db")

		LocalSQL.cursor().execute('''Create Table Config(
			LocalDirectory text not null
		)''')
		LocalSQL.cursor().execute('''Create Table Fetch(
			FetchID integer Primary Key AUTOINCREMENT,
			FetchUrl text not null,
			FetchTitle text not null,
			FetchCode text not null,
			FetchAA text not null,
			FetchTag text not null,
			FetchCover text not null,
			FetchSrc text not null,
			FetchSize integer not null,
			DateRegister text not null,
			TimeRegister text not null
		)''')
		LocalSQL.cursor().execute('''Create Table Download(
			DownloadID integer Primary Key AUTOINCREMENT,
			FetchID integer not null,
			DownloadPath text not null,
			DownloadCurrent integer not null,
			DownloadTotal integer not null,
			DateRegister text not null,
			TimeRegister text not null
		)''')
		LocalSQL.cursor().execute('''Create Table Account(
			AccountID integer Primary Key AUTOINCREMENT,
			AccountUrl text not null,
			AccountUsername text not null,
			AccountPassword text not null,
			AccountCache text not null,
			AccountCookies text not null,
			AccountStorage text not null,
			DateRegister text not null,
			TimeRegister text not null
		)''')

		LocalSQL.cursor().execute('''Insert into Config values (
			'{0}'
		)'''.format(
			os.path.dirname(os.path.realpath(__file__)) + "\\app.db"
		))

	else:
		LocalSQL = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\app.db")

		LocalSQL.cursor().execute('''Update Config set LocalDirectory='{0}' '''.format(
			os.path.dirname(os.path.realpath(__file__)) + "\\app.db"
		))
		LocalSQL.commit()

	App = QApplication(sys.argv)
	Config = MainWidget()

	Config.resize(500, 500)
	Config.setWindowTitle("PyDoujin Downloader Alpha 1.2_02")
	Config.show()

	App.exec_()