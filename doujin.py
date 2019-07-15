import os
import sys
import io
import requests
import json

from tqdm import tqdm
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
			getFilename = Image.split('/', 5)

			self.Download(Image, getFilename[5], '')

		os.chdir('../../../../')

		print('\n\nDownload Done!')
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
			self.Download('https://cdn.pururin.io/assets/images/data/' + getUrl_Data[4] + '/' + str(getPage) + '.' + getJSON['image_extension'], str(getPage), '.' + getJSON['image_extension'])

		os.chdir('../../../../')

		print('\n\nDownload Done!')
		print('Download Complete!')

	def Tsumino(self, Url):
		Request = HTMLSession().get(Url)
	
	def Url(self, _Url):
		temp = _Url.split('/', 4)

		if temp[2] == 'nhentai.net':
			self.nHentai(_Url)
		elif temp[2] == 'pururin.io':
			self.Pururin(_Url)
		# if temp[2] == 'tsumino.com':
		# 	self.Tsumino(_Url)

	def Download(self, Url, Filename, Extension):
		Download = requests.get(Url, stream=True)

		print('\nDownload Page No: ', Filename, ' ----> Downloading!')

		with open(Filename + Extension, 'wb') as x:
			for data in tqdm(iterable=Download.iter_content(chunk_size=1024), total=int(Download.headers['content-length'])/1024, unit="KB"):
				x.write(data)
			x.close()

		print('Download Page No: ', Filename, ' ----> Downloaded!')

	def CheckTitle(self, Title, Source):
		isTitleExist = os.path.isdir('Download/Doujin/' + Source + '/' + Title)

		if isTitleExist == True:
			os.chdir('Download/Doujin/' + Source + '/' + Title)
			print('Existing Directory Name of', Title)
		else:
			os.makedirs('Download/Doujin/' + Source + '/' + Title)
			os.chdir('Download/Doujin/' + Source + '/' + Title)
			print('Creating Directory Name of', Title)
