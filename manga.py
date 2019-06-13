import sys
import os
import io
import requests
import time
from requests_html import HTMLSession
from tqdm import tqdm

class Manga :

    def MangaTown(self, Url):
        Request = HTMLSession().get(Url)
        Title = Request.html.find('.title-top', first=True).text
        Chapter = Request.html.find('.chapter_list li')

        for getChapter in Chapter:
            temp_getChapter = getChapter.find('a', first=True).attrs['href'].split('/', 5)

            print(temp_getChapter)

            # _Page = HTMLSession().get('https:' + getChapter.find('a', first=True).attrs['href'])
            # Page = _Page.html.find('.page_select option')
            
            # for getPage in Page:
            #     _Image = HTMLSession().get('https:' + getPage.find('option', first=True).attrs['value'])
            #     Image = _Image.html.find('#viewer img', first=True).attrs['src'].split('?', 2)
            #     Download = HTMLSession().get(Image[0])
            #     Filename = getPage.find('option', first=True).text

    def MangaReader(self, Url):
        temp = (Url + '/').split('/', 4)

        #If There is a Chapter
        if temp[4] != "":
            GetTitle = HTMLSession().get('www.mangareader.net' + temp[3])
            Title = GetTitle.html.find('.aname', first=True).text
            Request = HTMLSession().get(Url)
            Page = Request.html.find('#pageMenu option')
            
            self.CheckChapter_and_Title(Title, temp[4])

            for getPage in Page:
                temp_getPage = getPage.find('option', first=True).attrs['value']
                _Image = HTMLSession().get('www.mangareader.net' + temp_getPage)
                Image = _Image.html.find('#imgholder img', first=True).attrs['src']
                    
                _Download = HTMLSession().get(Image)
                Filename = str(getPage.find('option', first=True).text) + '.jpg'

                print('Downloading : ' + Image)

                with open(Filename, 'wb') as x:
                    x.write(_Download.content)
                    x.close()

                print('Download Done!')

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

                for getPage in Page:
                    temp_getPage = getPage.find('option', first=True).attrs['value']
                    _Image = HTMLSession().get('https://www.mangareader.net' + temp_getPage)
                    Image = _Image.html.find('#imgholder img', first=True).attrs['src']
                    
                    _Download = HTMLSession().get(Image)
                    Filename = str(getPage.find('option', first=True).text) + '.jpg'
                    
                    print('Downloading : ' + Image)

                    with open(Filename, 'wb') as x:
                        x.write(_Download.content)
                        x.close()

                    print('Download Done!')

                os.chdir('..')

            print('Download Complete!')

    def MangaPanda(self, Url):
        temp = (Url + '/').split('/', 4)

        #If There is a Chapter
        if temp[4] != "":
            GetTitle = HTMLSession().get('https://www.mangapanda.com/' + temp[3])
            Title = GetTitle.html.find('.aname', first=True).text
            Request = HTMLSession().get(Url)
            Page = Request.html.find('#pageMenu option')
            
            self.CheckChapter_and_Title(Title, temp[4])

            for getPage in Page:
                temp_getPage = getPage.find('option', first=True).attrs['value']
                _Image = HTMLSession().get('https://www.mangapanda.com' + temp_getPage)
                Image = _Image.html.find('#imgholder img', first=True).attrs['src']
                    
                _Download = HTMLSession().get(Image)
                Filename = str(getPage.find('option', first=True).text) + '.jpg'

                print('Downloading : ' + Image)

                with open(Filename, 'wb') as x:
                    x.write(_Download.content)
                    x.close()

                print('Download Done!')

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

                for getPage in Page:
                    temp_getPage = getPage.find('option', first=True).attrs['value']
                    _Image = HTMLSession().get('https://www.mangapanda.com' + temp_getPage)
                    Image = _Image.html.find('#imgholder img', first=True).attrs['src']
                    
                    _Download = HTMLSession().get(Image)
                    Filename = str(getPage.find('option', first=True).text) + '.jpg'
                    
                    print('Downloading : ' + Image)

                    with open(Filename, 'wb') as x:
                        x.write(_Download.content)
                        x.close()

                    print('Download Done!')

                os.chdir('..')

            print('Download Complete!')

    def CheckTitle(self, Title):
        isTitleExist = os.path.isdir('Download/Manga/' + Title)
            
        if isTitleExist == True:
            os.chdir('Download/Manga/' + Title)
        else:
            os.makedirs('Download/Manga/' + Title)
            os.chdir('Download/Manga/' + Title)
    
    def CheckChapter(self, Chapter):
        isChapterExist = os.path.isdir(Chapter)

        if isChapterExist == True:
            os.chdir(str(Chapter))
                
        else:
            os.makedirs(str(Chapter))
            os.chdir(str(Chapter))

    def CheckChapter_and_Title(self, Title, Chapter):
        isTitleExist = os.path.isdir('Download/Manga/' + Title)
        isChapterExist = os.path.isdir('Download/Manga/' + Title + '/' + Chapter)
            
        if isTitleExist == True:
            os.chdir('Download/Manga/' + Title)

            if isChapterExist == True:
                os.chdir(str(Chapter))
            else:
                os.makedirs(str(Chapter))
                os.chdir(str(Chapter))

        else:
            os.makedirs('Download/Manga/' + Title)
            os.chdir('Download/Manga/' + Title)

            if isChapterExist == True:
                os.chdir(str(Chapter))
            else:
                os.makedirs(str(Chapter))
                os.chdir(str(Chapter))




        



# https://www.mangatown.com/manga/that_girl_is_not_just_cute
# http://www.mangahere.cc/manga/naka_no_hito_genome_jikkyouchuu/
# https://www.mangapanda.com/that-girl-is-not-just-cute
# https://www.mangareader.net/that-girl-is-not-just-cute