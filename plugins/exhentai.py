'''
Warning: This Script is really buggy sometimes
		 If you wanna use this script, Please upgrade your internet speed at the minimum of 25 Megabit per Second(Mbps) not Megabytes per Second(MBps)
		 Bit and Byte are different (8 bit is 1 bytes, 0 bit means logical off, 1 bit means logical on aka False(0) and True(1))

		 If this script is very buggy or error sometimes, Please Consult the Developers only

Author: Zeke Redgrave
'''
from bs4 import * #BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import requests

def load(self, getUrl=''):
	temp = {
		"Title": "",
		"Page": [],
		"Size": []
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

	getTotalImage = int(getFullHTML.find("p", { "class": "gpc"}).getText().split(" ")[len(getFullHTML.find("p", { "class": "gpc"}).getText().split(" ")) - 2])
	Count = 0

	if(int(getTotalImage / 20) == 0):
		for getPage in getFullHTML.find("div", { "id": "gdt"}).find_all("a"):
			eHentai_Login.get(getPage.get("href"))
			getFullHTML = BeautifulSoup(eHentai_Login.page_source, features="lxml")

			temp["Page"].append(getFullHTML.find("div", { "id":"i3" }).find("img", { "id":"img" }).get("src"))
			temp["Size"].append(requests.get(getFullHTML.find("div", { "id":"i3" }).find("img", { "id":"img" }).get("src"), stream=True).headers["content-length"])
				
			Count += 1

	else:
		for x in range(int(getTotalImage / 20) + 1):
			eHentai_Login.get(getUrl +"?p="+ str(x))
			getFullHTML = BeautifulSoup(eHentai_Login.page_source, features="lxml")

			for getPage in getFullHTML.find("div", { "id": "gdt"}).find_all("a"):
				eHentai_Login.get(getPage.get("href"))
				getFullHTML = BeautifulSoup(eHentai_Login.page_source, features="lxml")

				temp["Page"].append(getFullHTML.find("div", { "id":"i3" }).find("img", { "id":"img" }).get("src"))
				temp["Size"].append(requests.get(getFullHTML.find("div", { "id":"i3" }).find("img", { "id":"img" }).get("src"), stream=True).headers["content-length"])

				Count += 1

	eHentai_Login.quit()

	return temp