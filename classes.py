import os
import curses
import sys

class Window:
    wind = None
    header = ""
    body = ""
    footer = ""

    def __init__(self):
        print("Start wm")

    def menu(self, win, menuList, selectMenu):        
        self.wind = win

        win.nodelay(True)
        curses.curs_set(0)
        key = ""

        self.body = self.setMenu(menuList, selectMenu[0])
        self.updateWin()

        while True:
            try:
                key = win.getkey()

                if key == "KEY_DOWN":
                    selectMenu[0] += 1

                if key == "KEY_UP":
                    selectMenu[0] -= 1

                if selectMenu[0] == len(menuList):
                    selectMenu[0] = 0
                elif selectMenu[0] < 0:
                    selectMenu[0] = len(menuList)-1

                if key == "\n":
                    break

                self.body = self.setMenu(menuList, selectMenu[0])
                self.updateWin()
            except Exception as e:
                pass

    def setMenu(self, array, row):
        string = ""
        for i in range(len(array)):
            select = "[ ]"
            if i == row:
                select = "[*]"
            string += select+" "+array[i]+"\n"
        return string

    def updateWin(self):
        self.wind.clear()
        self.wind.addstr(self.header+self.body+self.footer)

    def showMenu(self, menuList):
        selectMenu = [0]
        curses.wrapper(self.menu, menuList, selectMenu)
        
        return selectMenu[0]
        

class Game:
    def __init__(self):
        print("start gm")
        self.win = Window()
        self.menu()

    def menu(self):
        self.win.header = "Игра крестики-нолики\nМеню:\n\n"
        menuList = ["Локальная", "Сетевая игра", "Инструкция", "Выход"]
        selectMenu = self.win.showMenu(menuList)

        if selectMenu == 3:
            exit()
        elif selectMenu == 2:
            self.info()
    
    def info(self):
        self.win.header = "Правила по игре\n\n"
        menuList = ["Назад"]
        selectMenu = self.win.showMenu(menuList)

        if selectMenu == 0:
            self.menu()