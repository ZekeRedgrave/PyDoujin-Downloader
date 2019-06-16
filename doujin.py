import os
import sys
import io
import requests
import json
from requests_html import HTMLSession


class Doujin:

	def nHentai(self, Url):
		Request = HTMLSession().get(Url)
		getID = Url.split('/', 5)
		Title = Request.html.find('#info h1', first=True).text
		Page = Request.html.find('#thumbnail-container div')

		self.CheckTitle(getID[4], 'nhentai')
		print('Downloading Doujin Name of', Title, '-', getID[4])

		for getPage in Page:
			_Image = HTMLSession().get('https://nhentai.net' + getPage.find('div a', first=True).attrs['href'])
			Image = _Image.html.find('#image-container img', first=True).attrs['src']

			Download = HTMLSession().get(Image)
			getFilename = Image.split('/', 5)

			with open(getFilename[5], 'wb') as x:
				x.write(Download.content)
				x.close()

		os.chdir('../../../../')

		print('Download Done!')
		print('Download Complete!')

	def Pururin(self, Url):
		Request = HTMLSession().get(Url)
		getUrl_Data = Url.split('/', 6)
		Title = Request.html.find('.title h1', first=True).text
		get_FirstPage = Request.html.find('#app .box a', first=True).attrs['href']

		_Page = HTMLSession().get(get_FirstPage)
		Page = _Page.html.find('gallery-read', first=True).attrs[':gallery']
		getJSON = json.loads(Page)

		self.CheckTitle(getUrl_Data[4], 'pururin')
		print('Downloading Doujin Name of', Title, '-', getUrl_Data[4])

		for getPage in range(1, int(getJSON['total_pages']) + 1):
			Download = HTMLSession().get('https://cdn.pururin.io/assets/images/data/' + getUrl_Data[4] + '/' + str(getPage) + '.' + getJSON['image_extension'])

			with open(str(getPage) + '.' + getJSON['image_extension'], 'wb') as x:
				x.write(Download.content)
				x.close()

		os.chdir('../../../../')

		print('Download Done!')
		print('Download Complete!')

	def CheckTitle(self, Title, Source):
		isTitleExist = os.path.isdir('Download/Doujin/' + Source + '/' + Title)

		if isTitleExist == True:
			os.chdir('Download/Doujin/' + Source + '/' + Title)
			print('Existing Directory Name of', Title)
		else:
			os.makedirs('Download/Doujin/' + Source + '/' + Title)
			os.chdir('Download/Doujin/' + Source + '/' + Title)
			print('Creating Directory Name of', Title)

# https://nhentai.net
# https://pururin.io/gallery/39617/fgo-no-ashibon-5
