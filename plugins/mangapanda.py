'''
Warning: This Script is really buggy sometimes
		 If you wanna use this script, Please upgrade your internet speed at the minimum of 25 Megabit per Second(Mbps) not Megabytes per Second(MBps)
		 Bit and Byte are different (8 bit is 1 bytes, 0 bit means logical off, 1 bit means logical on aka False(0) and True(1))

		 If this script is very buggy or error sometimes, Please Consult the Developers only

Author: Zeke Redgrave
'''
import requests
import concurrent.futures
import bs4

def load(getUrl=''):
	temp = {
		"Title" : "",
		"Code": getUrl.split("/")[3],
		"Tag": [],
		"Author/Artist": "",
		"Cover": "",
		"Src" : [],
		"Size" : []
	}
	getRaw = bs4.BeautifulSoup(requests.get("https://www.mangapanda.com/"+ getUrl.split("/")[3]).content, features="lxml")
	
	temp["Title"] = getRaw.find("table").find_all("tr")[0].find_all("td")[1].getText().replace("\n", "") + " " +str(getUrl.split("/")[4])
	temp["Tag"] = getRaw.find("table").find_all("tr")[7].find_all("td")[1].getText().replace("\n", " ").split(" ")
	temp["Author/Artist"] = getRaw.find("table").find_all("tr")[4].find_all("td")[1].getText().replace("\n", "") +"/"+ getRaw.find("table").find_all("tr")[5].find_all("td")[1].getText().replace("\n", "")
	temp["Cover"] = getRaw.find("div", {"id": "mangaimg"}).find("img").get("src")

	for x in bs4.BeautifulSoup(requests.get(getUrl).content, features="lxml").find("select", {"id":"pageMenu"}).find_all("option"):
		temp["Src"].append(bs4.BeautifulSoup(requests.get("https://www.mangapanda.com"+ x.get("value")).content, features="lxml").find("img", {"id":"img"}).get("src"))
		temp["Size"].append(requests.get(bs4.BeautifulSoup(requests.get("https://www.mangapanda.com"+ x.get("value")).content, features="lxml").find("img", {"id":"img"}).get("src"), stream=True).headers["content-length"])

	return temp