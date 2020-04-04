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

def load(self, getUrl=''):
	temp = {
		"Title": "",
		"Page": [],
		"Size" : []
	}

	r = HTMLSession().get(getUrl)

	temp["Title"] = r.html.find(".title", first=True).text
	findPage = r.html.find(".page_select select", first=True)
		
	for getPage in findPage.find("option"):
		if getPage.text.lower() in "featured":
			pass

		else:
			thread.append(concurrent.futures.ThreadPoolExecutor().submit(getImage, getPage.attrs['value']))

	for x in concurrent.futures.as_completed(thread):
		y = x.result()

		temp["Page"].append(y["Page"])
		temp["Size"].append(y["Size"])

	return temp
		

	return temp

def getImage(url):
	try:
		r = HTMLSession().get('http://www.mangatown.com' +url)

		return {
			"Page" : r.html.find("#viewer img", first=True).attrs['src'],
			"Size" : requests.get(r.html.find("#viewer img", first=True).attrs['src'], stream=True).headers['content-length']
		}

	except Exception as e:
		r = HTMLSession().get('http://www.mangatown.com' +url)
		_r = requests.get(r.html.find("#viewer img", first=True).attrs['src'], stream=True)

		for x in _r.headers:
			if str.lower(x) is "content-length":
				return {
					"Page" : r.html.find("#viewer img", first=True).attrs['src'],
					"Size" : _r.headers[x]
				}