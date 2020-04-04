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
		"Title" : "",
		"Page" : [],
		"Size" : []
	}
	thread = []

	r = HTMLSession().get(str(getUrl))

	temp["Title"] = r.html.find('#mangainfo .c3 h1', first=True).text
	findPage = r.html.find('#selectpage select', first=True)

	for getPage in findPage.find('option'):
		thread.append(concurrent.futures.ThreadPoolExecutor().submit(getImage, getPage.attrs['value']))

	for x in concurrent.futures.as_completed(thread):
		y = x.result()

		temp["Page"].append(y["Page"])
		temp["Size"].append(y["Size"])

	return temp

def getImage(url):
	try:
		r = HTMLSession().get('http://www.mangareader.net' +url)

		return {
			"Page" : r.html.find('#imgholder img', first=True).attrs['src'],
			"Size" : requests.get(r.html.find('#imgholder img', first=True).attrs['src'], stream=True).headers['content-length']
		}

	except Exception as e:
		r = HTMLSession().get('http://www.mangareader.net' +url)
		_r = requests.get(r.html.find('#imgholder img', first=True).attrs['src'], stream=True)

		for x in _r.headers:
			if str.lower(x) is "content-length":
				return {
					"Page" : r.html.find('#imgholder img', first=True).attrs['src'],
					"Size" : _r.headers[x]
				}
