'''
Warning: This Script is really buggy sometimes
		 If you wanna use this script, Please upgrade your internet speed at the minimum of 25 Megabit per Second(Mbps) not Megabytes per Second(MBps)
		 Bit and Byte are different (8 bit is 1 bytes, 0 bit means logical off, 1 bit means logical on aka False(0) and True(1))

		 If this script is very buggy or error sometimes, Please Consult the Developers only

Author: Zeke Redgrave
'''
from requests_html import HTMLSession
from tqdm import tqdm

import os
import io
import json
import requests

class mangareader:
	def load(self, getUrl=''):
		temp = {
			"Title" : "",
			"Page" : [],
			"Size" : []
		}
		r = HTMLSession().get(str(getUrl))

		temp["Title"] = r.html.find('#mangainfo .c3 h1', first=True).text
		findPage = r.html.find('#selectpage select', first=True)

		for getPage in findPage.find('option'):
			r = HTMLSession().get('http://www.mangareader.net' +getPage.attrs['value'])
			_r = requests.get(r.html.find('#imgholder img', first=True).attrs['src'], stream=True)

			temp["Page"].append(r.html.find('#imgholder img', first=True).attrs['src'])

			try:
				temp["Size"].append(_r.headers['content-length'])

			except Exception as e:
				for x in _r.headers:
					if str.lower(x) is "content-length":
						temp["Size"].append(_r.headers[x])

		return temp
