import sys
import os
import io
import requests
import json

from tqdm import tqdm
from requests_html import HTMLSession

class Manga :

    def MangaReader(self, Url):
        temp = (Url + '/').split('/', 4)

        #If There is a Chapter
        if temp[4] != "":
            GetTitle = HTMLSession().get('https://www.mangareader.net/' + temp[3])
            Title = GetTitle.html.find('.aname', first=True).text
            Request = HTMLSession().get(Url)
            Page = Request.html.find('#pageMenu option')

            self.CheckTitle(Title)
            self.CheckChapter(temp[4].replace('/', ''))
            print('Download Chapter No# ', temp[4].replace('/', ''))

            for getPage in Page:
                temp_getPage = getPage.find('option', first=True).attrs['value']
                _Image = HTMLSession().get('https://www.mangareader.net' + temp_getPage)
                Image = _Image.html.find('#imgholder img', first=True).attrs['src']
                Filename = str(getPage.find('option', first=True).text)

                self.Download(Image, Filename, '.jpg')

            os.chdir('../../../../')
            print('\n\nDownload Done!')
            print('Download Complete!')

        #If Not has Chapter only Title
        else:
            Request = HTMLSession().get(Url)
            Chapter = Request.html.find('#listing a')
            Title = Request.html.find('.aname', first=True).text
            
            self.CheckTitle(Title)

            for getChapter in Chapter:
                temp_getChapter = getChapter.find('a', first=True).attrs['href'].split('/', 2)
                _Page = HTMLSession().get(Url + '/' + temp_getChapter[2])
                Page = _Page.html.find('#pageMenu option')

                self.CheckChapter(temp_getChapter[2])
                print('Download Chapter No# ', temp_getChapter[2])

                for getPage in Page:
                    temp_getPage = getPage.find('option', first=True).attrs['value']
                    _Image = HTMLSession().get('https://www.mangareader.net' + temp_getPage)
                    Image = _Image.html.find('#imgholder img', first=True).attrs['src']
                    Filename = str(getPage.find('option', first=True).text)

                    self.Download(Image, Filename, '.jpg')

                os.chdir('..')
                print('\n\nDownload Done!')

            os.chdir('../../../')
            print('Download Complete!')

    def MangaPanda(self, Url):
        temp = (Url + '/').split('/', 4)

        #If There is a Chapter
        if temp[4] != "":
            GetTitle = HTMLSession().get('https://www.mangapanda.com/' + temp[3])
            Title = GetTitle.html.find('.aname', first=True).text
            Request = HTMLSession().get(Url)
            Page = Request.html.find('#pageMenu option')

            self.CheckTitle(Title)
            self.CheckChapter(temp[4].replace('/', ''))

            print('Download Chapter No# ', temp[4].replace('/', ''))

            for getPage in Page:
                temp_getPage = getPage.find('option', first=True).attrs['value']
                _Image = HTMLSession().get('https://www.mangapanda.com' + temp_getPage)
                Image = _Image.html.find('#imgholder img', first=True).attrs['src']
                    
                Filename = str(getPage.find('option', first=True).text)

                self.Download(Image, Filename, '.jpg')

            os.chdir('../../../../')
            print('\n\nDownloaded!')
            print('Download Complete!')

        #If Not has Chapter only Title
        else:
            Request = HTMLSession().get(Url)
            Chapter = Request.html.find('#listing a')
            Title = Request.html.find('.aname', first=True).text
            
            self.CheckTitle(Title)

            for getChapter in Chapter:
                temp_getChapter = getChapter.find('a', first=True).attrs['href'].split('/', 2)
                _Page = HTMLSession().get(Url + '/' + temp_getChapter[2])
                Page = _Page.html.find('#pageMenu option')

                self.CheckChapter(temp_getChapter[2])
                print('Download Chapter No# ', temp_getChapter[2])

                for getPage in Page:
                    temp_getPage = getPage.find('option', first=True).attrs['value']
                    _Image = HTMLSession().get('https://www.mangapanda.com' + temp_getPage)
                    Image = _Image.html.find('#imgholder img', first=True).attrs['src']
                    
                    Filename = str(getPage.find('option', first=True).text)

                    self.Download(Image, Filename, '.jpg')

                os.chdir('..')
                print('\n\nDownload Done!')
            os.chdir('../../../')
            print('Download Complete!')

    def MangaTown(self, Url):
        temp = (Url + '/').split('/', 6)

        # If Chapter Exist
        if temp[5] != "" :
            Request = HTMLSession().get('https://www.mangatown.com/manga/' + temp[4] + '/')
            Title = Request.html.find('.title-top', first=True).text
            temp_getChapter = Url.split('/', 6)
            temp_ChapterID = temp_getChapter[5].split('c', 1)
            ChapterName = temp_ChapterID[1].split('0', 1)
            RemoveDot = str(float(ChapterName[1])).split('.0', 1)

            self.CheckTitle(Title)
            self.CheckChapter(RemoveDot[0])

            print('Download Chapter No# ', RemoveDot[0])
            _Page = HTMLSession().get(Url)
            Page = _Page.html.find('.page_select option')

            for getPage in Page:
                _Image = HTMLSession().get('https:' + getPage.find('option', first=True).attrs['value'])
                getFeature = getPage.find('option', first=True).attrs['value'].split('/', 6)

                if(getFeature[6] != 'featured.html'):
                    Image = _Image.html.find('#viewer img', first=True).attrs['src']
                    Filename = getPage.find('option', first=True).text

                    self.Download(Image, Filename, '.jpg')
                else:
                    break

            os.chdir('../../../../')
            print('\n\nDownloaded!')
            print('Download Complete!')

        else:
            Request = HTMLSession().get(Url)
            Title = Request.html.find('.title-top', first=True).text
            Chapter = Request.html.find('.chapter_list li')

            self.CheckTitle(Title)

            for getChapter in Chapter:
                temp_getChapter = getChapter.find('a', first=True).attrs['href'].split('/', 6)
                temp_ChapterID = temp_getChapter[5].split('c', 1)
                ChapterName = temp_ChapterID[1].split('0', 1)
                RemoveDot = str(float(ChapterName[1])).split('.0', 1)

                self.CheckChapter(RemoveDot[0])
                print('Download Chapter No# ', RemoveDot[0])

                _Page = HTMLSession().get('https:' + getChapter.find('a', first=True).attrs['href'])
                Page = _Page.html.find('.page_select option')

                for getPage in Page:
                    _Image = HTMLSession().get('https:' + getPage.find('option', first=True).attrs['value'])
                    getFeature = getPage.find('option', first=True).attrs['value'].split('/', 6)

                    if(getFeature[6] != 'featured.html'):
                        Image = _Image.html.find('#viewer img', first=True).attrs['src']
                        Filename = getPage.find('option', first=True).text

                        self.Download(Image, Filename, '.jpg')
                    else:
                        break

                os.chdir('..')
                print('\n\nDownloaded!')

            os.chdir('../../../')
            print('Download Complete!')

    def MangaHere(self, Url):
        temp = Url.replace('mangahere.cc', 'mangatown.com')
        self.MangaTown(temp)

    def Url(self, _Url):
        temp = _Url.split('/', 4)

        if temp[2] == 'www.mangapanda.com':
            self.MangaPanda(_Url)
        elif temp[2] == 'www.mangareader.net':
            self.MangaReader(_Url)
        elif temp[2] == 'www.mangatown.com':
            self.MangaTown(_Url)
        elif temp[2] == 'www.mangahere.cc':
            self.MangaHere(_Url)

    def Download(self, Url, Filename, Extension):
        Download = requests.get(Url, stream=True)
        Size = int(Download.headers['content-length'])

        print('\nDownload Page No: ', Filename, ' ----> Downloading!')

        with open(Filename + Extension, 'wb') as x:
            for data in tqdm(iterable=Download.iter_content(chunk_size=1024), total=int(Download.headers['content-length'])/1024, unit="KB"):
                x.write(data)

            x.close()
        print('Download Page No: ', Filename, ' ----> Downloaded!')

    def CheckTitle(self, Title):
        isTitleExist = os.path.isdir('Download/Manga/' + Title)
            
        if isTitleExist == True:
            os.chdir('Download/Manga/' + Title)
            print('Existing Directory Name of', Title)
        else:
            os.makedirs('Download/Manga/' + Title)
            os.chdir('Download/Manga/' + Title)
            print('Creating Directory Name of', Title)
    
    def CheckChapter(self, Chapter):
        isChapterExist = os.path.isdir(Chapter)

        if isChapterExist == True:
            os.chdir(str(Chapter))
            print('Existing Directory Name of', Chapter)
                
        else:
            os.makedirs(str(Chapter))
            os.chdir(str(Chapter))
            print('Creating Directory Name of', Chapter)
