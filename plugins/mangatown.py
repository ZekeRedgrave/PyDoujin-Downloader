from requests_html import HTMLSession
from tqdm import tqdm

import os
import io
import json
import requests

class mangatown:
	def load(self, getUrl=''):
		temp = {
			"Title": "",
			"Page": []
		}

		r = HTMLSession().get(getUrl)

		temp["Title"] = r.html.find(".title", first=True).text
		findPage = r.html.find(".page_select select", first=True)
		
		for getPage in findPage.find("option"):
			if getPage.text.lower() in "featured":
				break

			else:
				r = HTMLSession().get("https://www.mangatown.com"+ getPage.attrs['value'])

				temp["Page"].append(r.html.find("#viewer img", first=True).attrs['src'])

		return temp