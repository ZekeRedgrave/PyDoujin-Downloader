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
			"Page" : []
		}
		r = HTMLSession().get(str(getUrl))

		temp["Title"] = r.html.find('#mangainfo .c3 h1', first=True).text
		findPage = r.html.find('#selectpage select', first=True)

		for getPage in findPage.find('option'):
			r = HTMLSession().get('http://www.mangareader.net' +getPage.attrs['value'])
			temp["Page"].append(r.html.find('#imgholder img', first=True).attrs['src'])

		return temp
