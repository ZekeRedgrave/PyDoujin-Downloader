from requests_html import HTMLSession
from tqdm import tqdm

import os
import io
import json
import requests

class mangafox:
	def load(self, getUrl=''):
		temp = {
			"Title": "",
			"Page": []
		}
		r = HTMLSession().get(getUrl)

		temp["Title"] = r.html.find("title", first=True).text.replace(' Chapter', '')
		findPage = r.html.find(".list_img", first=True)

		for getPage in findPage.find("img"):
			temp["Page"].append(getPage.attrs['src'])

		return temp