import sys
import os
import manga
import doujin

class Area:
    # Help Area
    def HelpArea(self):
        Nav = ''

        for x in range(0, 60):
            Nav = Nav + '-'

        print(Nav)
        print('Hacker-chan Help Guide')
        print(Nav)
        print('\n\tManga -----> Manga <URL> Ex. Manga https://manga.com/my-manga-title || https://manga.com/my-manga-title/chapter-1/')
        print('\tDoujin -----> Doujin <URL> Ex. Doujin https://manga.com/my-doujin-title')
        print('\tExit -----> Terminate the Program\n\n')

        print(Nav)
        print('Web can Allowed to Download')
        print(Nav)

        
        
        os.system('pause')
        os.system('cls')
        
        print('Console Application Version Alpha 5')
        print('Hacker-chan\n')
        print('Type "help" for more info\n\n')

        self.MenuArea()

    # End of Help Area
    # Menu Area
    def MenuArea(self):
        Say = input('\n\nConsole >> ').lower().split(' ')

        if Say[0] == 'manga':
            x = manga.Manga()
            x.Url(Say[1])

            self.MenuArea()
        elif Say[0] == 'doujin':
            x = doujin.Doujin()
            x.Url(Say[1])

            self.MenuArea()
        elif Say[0] == 'help':
            os.system('cls')

            self.HelpArea()
        elif Say[0] == 'exit':
            pass
        else:
            self.MenuArea()
