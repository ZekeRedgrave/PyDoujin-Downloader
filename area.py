import sys
import os
import manga
import doujin

class Area:
    MangaDictionary = ['www.mangareader.net', 'www.mangapanda.com', 'www.mangahere.cc', 'www.mangatown.com']
    DoujinDictionary = ['nhentai.net', 'pururin.io']
    # Manga Area
    def MangaArea(self):
        x = manga.Manga()

        os.system('cls')

        print('Hacker-chan Manga')
        print('[1 -> Search URL] || [2 -> List] || [0 -> Back]')
        Say = int(input('Say >> '))

        if Say == 1:
            URL = input('\n\nManga URL : ')
            
            temp = URL.split('/', 3)
            #MangaReader
            if temp[2] == self.MangaDictionary[0]:
                x.MangaReader(URL)
                self.MangaArea()
            #MangaPanda 
            elif temp[2] == self.MangaDictionary[1]:
                x.MangaPanda(URL)
                self.MangaArea()
            #MangaHere
            elif temp[2] == self.MangaDictionary[2]:
                x.MangaHere(URL)
                self.MangaArea()
            #MangaTown 
            elif temp[2] == self.MangaDictionary[3]:
                x.MangaTown(URL)
                self.MangaArea()
            
            elif URL == 'exit()':
                self.MenuArea()
            elif int(URL) == 0:
                self.MangaArea()
            else:
                print('Error >> Not Available for Web Scraping!')
                self.MangaArea()

        elif Say == 0:
            self.MenuArea()
        else:
            self.MangaArea()
    # End of Manga Area
    # Doujin Area
    def DoujinArea(self):
        x = doujin.Doujin()

        os.system('cls')

        print('Hacker-chan Doujin\n')
        print('[1 -> Search URL] || [2 -> List] || [0 -> Back]')
        Say = int(input('Say >> '))

        if Say == 1:
            URL = input('\n\nDoujin URL : ')

            temp = URL.split('/', 3)
            
            #nHentai
            if temp[2] == self.DoujinDictionary[0]:
                x.nHentai(URL)
                self.DoujinArea()
            #Pururin
            if temp[2] == self.DoujinDictionary[1]:
                x.Pururin(URL)
                self.DoujinArea()
            elif URL == 'exit()':
                self.MenuArea()
            elif int(URL) == 0:
                self.DoujinArea()
            else:
                print('Error >> Not Available for Web Scraping!')
                self.DoujinArea()
        elif Say == 0:
            self.MenuArea()
        else:
            self.MangaArea()
    #End of Doujin Area
    # Menu Area
    def MenuArea(self):
        os.system('cls')
        print('Console Application Version Alpha 3')
        print('Hacker-chan Menu\n')
        print('[1 -> Search URL] || [2 -> Manga] || [3 -> Doujin] || [0 -> Exit]')
        Say = int(input('Say >> '))

        if Say == 0:
            print('Bye')
        elif Say == 2:
            self.MangaArea()
        elif Say == 3:
            self.DoujinArea()
        else:
            self.MenuArea() 
    # End of Menu Area
        
            