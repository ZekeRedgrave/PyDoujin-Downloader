import sys
import os
import manga

class Area:
    MangaDictionary = ['www.mangareader.net', 'www.mangapanda.com', 'www.mangahere.cc', 'www.mangatown.com']
    # Manga Area
    def MangaArea(self):
        x = manga.Manga()

        os.system('cls')

        print('Hacker-chan Manga\n')
        print('[1 -> Search URL] || [2 -> List] || [0 -> Back]')
        Say = int(input('Say >> '))

        if Say == 1:
            URL = input('\n\n Manga URL : ')
            
            temp = URL.split('/', 3)
            #MangaReader
            if temp[2] == self.MangaDictionary[0]:
                x.MangaReader(URL)
            #MangaPanda 
            elif temp[2] == self.MangaDictionary[1]:
                x.MangaPanda(URL)
            #MangaTown 
            elif temp[2] == self.MangaDictionary[3]:
                x.MangaTown(URL)
            elif URL == 'exit()':
                self.MenuArea()
            elif int(URL) == 0:
                self.MangaArea()
            else:
                print('Error >> Invalid URL!')
                self.MangaArea()

        elif Say == 0:
            self.MenuArea()
        else:
            self.MangaArea()

    # End of Manga Area
    # Menu Area
    def MenuArea(self):
        os.system('cls')
        print('Console Application Version Alpha 2')
        print('Hacker-chan Menu\n')
        print('[1 -> Search URL] || [2 -> Manga] || [3 -> Doujin] || [0 -> Exit]')
        Say = int(input('Say >> '))

        if Say == 0:
            print('Bye')
        elif Say == 2:
            self.MangaArea()
        elif Say == 3:
            print('Error >> This Feature is Not Available!')

            self.MenuArea()
        else:
            self.MenuArea() 
    # End of Menu Area
        
            