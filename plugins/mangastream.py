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
		"Code": getUrl.split("/")[5],
		"Tag": [],
		"Author/Artist": "",
		"Cover": "",
		"Src" : [],
		"Size" : []
	}
	getRaw = bs4.BeautifulSoup(requests.get("https://www.mangastream.cc/manga/"+ getUrl.split("/")[4]).content, features="lxml")

	temp["Title"] = getRaw.find("div", {"class":"post-title"}).getText().strip('\n\t').strip()+ " " +str(getUrl.split("/")[5].split("-")[len(getUrl.split("/")[5].split("-")) - 1])
	temp["Author/Artist"] = ( getRaw.find("div", {"class":"author-content"}).getText()+ "/" +getRaw.find("div", {"class":"artist-content"}).getText() ).strip('\n\t').strip()
	temp["Cover"] = getRaw.find("div", {"class":"summary_image"}).find("img").get("src")
	for x in getRaw.find("div", {"class":"genres-content"}).getText().split(","):
		temp["Tag"].append(x.strip('\n\t').strip())

	for x in bs4.BeautifulSoup(requests.get(getUrl).content, features="lxml").find("div", {"class": "page-break"}).find_all("img"):
		temp["Src"].append(x.get("src"))
		temp["Size"].append(requests.get(x.get("src"), stream=True).headers["content-length"])

	return temp