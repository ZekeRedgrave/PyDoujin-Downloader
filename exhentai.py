from bs4 import * #BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import time
import requests
import re


class exhentai:
	def load(self, getUrl=''):
		temp = {
			"Title": "",
			"Page": []
		}
		headers = {
			"User-Agent" : "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
		}

		dcap = dict(DesiredCapabilities.PHANTOMJS)
		dcap["phantomjs.page.settings.userAgent"] = (headers["User-Agent"])
		eHentai_Login = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=os.path.dirname(os.path.realpath(__file__)) + '/phantomjs.exe')

		# options = webdriver.ChromeOptions()
		# options.add_argument('"--headless"')
		# eHentai_Login = webdriver.Chrome(chrome_options=options, executable_path=os.path.dirname(os.path.realpath(__file__)) + '/chromedriver.exe')

		eHentai_Login.get("https://forums.e-hentai.org/index.php?act=Login&CODE=00")
		# Login Session for e-forum
		eHentai_Username = eHentai_Login.find_element_by_name("UserName")
		eHentai_Password = eHentai_Login.find_element_by_name("PassWord")
		eHentai_Username.send_keys("megadestro") # Username
		eHentai_Password.send_keys("Stephen21") # Password
		eHentai_Login.find_element_by_name("submit").click()
		getFullHTML = BeautifulSoup(eHentai_Login.page_source, features="lxml")
		eHentai_Login.get(getFullHTML.find("a").get("href"))
		eHentai_Login.get("https://exhentai.org/")
		eHentai_Login.execute_script("window.localStorage.clear();")
		eHentai_Login.get(getUrl)

		getFullHTML = BeautifulSoup(eHentai_Login.page_source, features="lxml")
		temp["Title"] = getFullHTML.find(id="gn").getText().translate(str.maketrans("", "", '/\:*?<>|'))[:100] if len(getFullHTML.find(id="gn").getText().translate(str.maketrans("", "", '/\:*?<>|'))) <= 100 else getFullHTML.find(id="gj").getText().translate(str.maketrans("", "", '/\:*?<>|'))
		# Windows filename only reached 112 characters length ^

		getTotalImage = int(len(getFullHTML.find("p", { "class": "gpc"}).getText().split(" ")[len(getFullHTML.find("p", { "class": "gpc"}).getText().split(" ")) - 2]) / 20)
		Count = 0

		if(int(getTotalImage / 20) == 0):
			for getPage in getFullHTML.find("div", { "id": "gdt"}).find_all("a"):
				eHentai_Login.get(getPage.get("href"))
				getFullHTML = BeautifulSoup(eHentai_Login.page_source, features="lxml")

				temp["Page"].append(getFullHTML.find("div", { "id":"i3" }).find("img", { "id":"img" }).get("src"))

		else:
			for x in range(int(getTotalImage / 20)):
				eHentai_Login.get(getUrl +"?p="+ str(x))
				getFullHTML = BeautifulSoup(eHentai_Login.page_source, features="lxml")

				for getPage in getFullHTML.find("div", { "id": "gdt"}).find_all("a"):
					eHentai_Login.get(getPage.get("href"))
					getFullHTML = BeautifulSoup(eHentai_Login.page_source, features="lxml")

					temp["Page"].append(getFullHTML.find("div", { "id":"i3" }).find("img", { "id":"img" }).get("src"))

		return temp