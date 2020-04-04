'''
Warning: This Script is really buggy sometimes
		 If you wanna use this script, Please upgrade your internet speed at the minimum of 25 Megabit per Second(Mbps) not Megabytes per Second(MBps)
		 Bit and Byte are different (8 bit is 1 bytes, 0 bit means logical off, 1 bit means logical on aka False(0) and True(1))

		 If this script is very buggy or error sometimes, Please Consult the Developers only

Author: Zeke Redgrave
'''
from requests_html import HTMLSession

import requests
import concurrent.futures

def load(getUrl=''):
	temp = {
		"Title" : "",
		"Page" : [],
		"Size" : []
	}
	Thread = []

	r = HTMLSession().get(str(getUrl))
	temp["Title"] = r.html.find(".navbar h1", first=True).text

	for x in range(1, int(r.html.find(".content a", first=True).attrs["href"].split("/")[2].split("-")[6].split(".")[0]) + 1):
		Thread.append(concurrent.futures.ThreadPoolExecutor().submit(getImage, getUrl +"image-hgamecg-" +LeadingZeros_Format(x, 4)+ "-id-" +str(x)+ "-pics-" +str(r.html.find(".content a", first=True).attrs["href"].split("/")[2].split("-")[6].split(".")[0])+ ".html"))

	for x in concurrent.futures.as_completed(Thread):
		y = x.result()

		temp["Page"].append(y["Page"])
		temp["Size"].append(y["Size"])

	return temp

def getImage(url=''):
	try:
		r = HTMLSession().get(str(url))

		return {
			"Page" : r.html.find("img", first=True).attrs["src"],
			"Size" : requests.get(r.html.find("img", first=True).attrs["src"], stream=True).headers["content-length"]
		}

	except Exception as e:
		r = HTMLSession().get(str(url))
		_r = requests.get(r.html.find("img", first=True).attrs["src"], stream=True)

		for x in _r.headers:
			if str.lower(x) is "content-length":
				return {
					"Page" : r.html.find('#imgholder img', first=True).attrs['src'],
					"Size" : _r.headers[x]
				}

def LeadingZeros_Format(num, size):
	s = str(num) + ""

	while len(s) < size:
		s = "0" + s

	return s