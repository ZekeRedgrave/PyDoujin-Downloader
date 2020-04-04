'''
Warning: This Script is really buggy sometimes
		 If you wanna use this script, Please upgrade your internet speed at the minimum of 25 Megabit per Second(Mbps) not Megabytes per Second(MBps)
		 Bit and Byte are different (8 bit is 1 bytes, 0 bit means logical off, 1 bit means logical on aka False(0) and True(1))

		 If this script is very buggy or error sometimes, Please Consult the Developers only

Author: Zeke Redgrave
'''
from requests_html import HTMLSession

import requests

def load( getUrl=''):
	temp = {
		"Title": "",
		"Page": [],
		"Size" : []
	}

	r = HTMLSession().get(getUrl)

	temp["Title"] = r.html.find("title", first=True).text.replace(' Chapter', '')
	findPage = r.html.find(".list_img", first=True)

	for getPage in findPage.find("img"):
		_r = requests.get(getPage.attrs['src'], stream=True)

		temp["Page"].append(getPage.attrs['src'])

		try:
			temp["Size"].append(_r.headers['content-length'])

		except Exception as e:
			for x in _r.headers:
				if str.lower(x) is "content-length":
					temp["Size"].append(_r.headers[x])

	return temp