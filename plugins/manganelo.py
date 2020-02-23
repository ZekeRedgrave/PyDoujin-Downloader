from requests_html import HTMLSession
from tqdm import tqdm

import os
import io
import json
import requests

class manganelo:
	def load(self, getUrl=''):
		temp = {
			"Title": "",
			"Page": []
		}
		r = HTMLSession().get(getUrl)

		temp["Title"] = r.html.find("title", first=True).text.split('-')[0][:len(r.html.find("title", first=True).text.split('-')[0]) - 1]
		findPage = r.html.find(".container-chapter-reader", first=True)

		for getPage in findPage.find("img"):
			temp["Page"].append(getPage.attrs['src'])

		return temp