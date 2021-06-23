import os
import curses
import copy

class Window:
    wind = None
    header = ""
    body = ""
    footer = ""

    colorUser1 = 2
    colorUser2 = 208
    selectColor = 241
    bgColor = curses.COLOR_BLACK #241
    textColor = 255

    backButton = ("\x1b", "q", "Q")
    topButton = ("KEY_UP")

    def __init__(self):
        print("Start window")

    # START menu
    def showMenu(self, menuList):
        selectMenu = [0]
        curses.wrapper(self.menu, menuList, selectMenu)
        return selectMenu[0]

    def menu(self, win, menuList, selectMenu):
        self.setSetting(win)
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

                if key in self.backButton:
                    selectMenu[0] = len(menuList)-1
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
    # END menu

    # START other function
    def updateWin(self):
        self.wind.clear()
        self.wind.addstr(self.header+"\n", curses.color_pair(1) | curses.A_BOLD)
        self.wind.addstr(self.body+"\n"+self.footer, curses.color_pair(1))
        
    
    def setSetting(self, win):
        self.wind = win
        self.wind.nodelay(True)
        curses.curs_set(0)
        curses.init_pair(1, self.textColor, self.bgColor)
        self.wind.bkgd(' ', curses.color_pair(1))
    
    def clear(self):
        self.header = ""
        self.body = ""
        self.footer = ""
        # self.updateWin()
    # END other function

    # START body text
    def showBodyText(self, sring):
        key = [""]
        curses.wrapper(self.text, sring, key)
        return key[0]

    def text(self, win, sring, key):
        self.setSetting(win)

        self.body = sring
        self.updateWin()

        while True:
            try:
                key[0] = win.getkey()
                break
            except Exception as e:
                pass
    # END body text

    # START game field
    def showGameField(self, arrayField, user, setRow, setLine):
        xy = ["", ""]
        curses.wrapper(self.gameField, arrayField, xy, user, setRow, setLine)
        return xy[0], xy[1]

    def gameField(self, win, arrayField, xy, user, setRow, setLine):
        self.setSetting(win)
        
        curses.init_pair(5, self.textColor, self.selectColor)
        curses.init_pair(6, self.colorUser1, self.bgColor)
        curses.init_pair(7, self.colorUser1, self.selectColor)
        curses.init_pair(8, self.colorUser2, self.bgColor)
        curses.init_pair(9, self.colorUser2, self.selectColor)

        self.createGrid(win, arrayField, setLine, setRow, user) 

        while True:
            try:
                key = win.getkey()

                if key == "KEY_DOWN" and setLine < len(arrayField)-1:
                    setLine += 1

                if key == "KEY_UP" and setLine > 0:
                    setLine -= 1

                if key == "KEY_RIGHT" and setRow < len(arrayField)-1:
                    setRow += 1

                if key == "KEY_LEFT" and setRow > 0:
                    setRow -= 1

                if key == "\n":
                    xy[0] = setLine
                    xy[1] = setRow
                    arrayField[setLine][setRow] = user
                    break

                if key in self.backButton:
                    xy[0] = -1
                    xy[1] = -1
                    break

                self.createGrid(win, arrayField, setLine, setRow, user) 
            except Exception as e:
                pass
        
    def createGrid(self, win, arrayField, setLine, setRow, user):
        win.clear()
        win.addstr(self.header+"\n", curses.color_pair(1) | curses.A_BOLD)
        win.addstr("Ходит игрок ", curses.color_pair(1))
        if user == "X":
            win.addstr(user, curses.color_pair(6) | curses.A_BOLD)
        elif user == "O":
            win.addstr(user, curses.color_pair(8) | curses.A_BOLD)
        win.addstr("\n\n")

        string = ""
        lineInt = 0
        for line in arrayField:
            rowInt = 0 
            for row in line:
                if rowInt == setRow and lineInt == setLine:
                    if row == "X":
                        win.addstr(" "+row+" ", curses.color_pair(7) | curses.A_BOLD)
                    elif row == "O":
                        win.addstr(" "+row+" ", curses.color_pair(9) | curses.A_BOLD)
                    else:
                        win.addstr(" "+row+" ", curses.color_pair(5))
                else:
                    if row == "X":
                        win.addstr(" "+row+" ", curses.color_pair(6) | curses.A_BOLD)
                    elif row == "O":
                        win.addstr(" "+row+" ", curses.color_pair(8) | curses.A_BOLD)
                    else:
                        win.addstr(" "+row+" ", curses.color_pair(1))
                
                if rowInt < len(line)-1:
                    win.addstr("│", curses.color_pair(1))
                rowInt += 1

            if lineInt < len(arrayField)-1:
                endString = ""
                for i in range(len(line)):
                    if i < len(line)-1:
                        endString += "───┼"
                    else:
                        endString += "───"

                win.addstr("\n"+endString+"\n", curses.color_pair(1))
            lineInt += 1
        win.addstr("\n\n"+self.footer, curses.color_pair(1))
    # END game field

class Game:
    lenGrid = 3
    endGameCount = 3

    def __init__(self):
        print("Start game")
        self.default()
        self.win = Window()
        self.menuPage()

    def default(self):
        self.arrayField = [[" " for x in range(self.lenGrid)] for y in range(self.lenGrid)]
        self.user = "X"
        self.setLine, self.setRow = 1, 1
        

    def menuPage(self):
        self.win.clear()
        self.win.header = "Игра крестики-нолики\nМеню:\n"
        self.win.footer = "Для выхода нажмите кнопку ESC или q"
        menuList = ["Локальная", "Сетевая игра", "Инструкция", "Выход"]
        selectMenu = self.win.showMenu(menuList)

        if selectMenu == 3:
            exit()
        elif selectMenu == 2:
            self.infoPage()
        elif selectMenu == 1:
            self.interGame()
        elif selectMenu == 0:
            self.localGame()
    
    def infoPage(self):
        self.win.header = "Правила по игре\n\n"
        menuList = ["Назад"]
        selectMenu = self.win.showMenu(menuList)

        if selectMenu == 0:
            self.menuPage()
    
    def localGame(self, footer=""):
        self.win.clear()
        self.win.header = "Локальная игра вдвоем"
        self.win.footer = footer+"Чтобы вернуться в меню нажмите кнопку ESC или q"
        arrayFunField = copy.deepcopy(self.arrayField)
        self.setLine, self.setRow = self.win.showGameField(arrayFunField, self.user, self.setRow, self.setLine)

        if self.setLine < 0 and self.setRow < 0:
            self.default()
            self.menuPage()
        
        if self.arrayField[self.setLine][self.setRow] != " ":
            self.localGame("Данная ячейка уже занята\n")
        else:
            self.arrayField[self.setLine][self.setRow] = self.user

        endGame = self.endGame()
        if endGame == 0:
            # continue game

            if self.user == "X":
                self.user = "O"
            else:
                self.user = "X"

            self.localGame()
        else:
            # end game
            self.win.clear()
            self.win.header = "Победил игрок: "+self.user
            if endGame == 2:
                self.win.header = "Ничья"
            menuList = ["Заново", "Главное меню"]
            selectMenu = self.win.showMenu(menuList)
            if selectMenu == 1:
                self.menuPage()
            elif selectMenu == 0:
                self.default()
                self.localGame()
        
    def interGame(self):
        print()

    def endGame(self):
        # return options:
        # 0 - continue game
        # 1 - end game
        # 2 - draw

        lenFor = self.lenGrid - self.endGameCount + 1
        checkArray = [self.user]*self.endGameCount

        # horizontal check
        for i in range(lenFor):
            if self.arrayField[self.setLine][i:self.endGameCount+i] == checkArray:
                return 1
        
        # vertical check
        for i in range(lenFor):
            verticalArray = []
            for lineInt in range(i, self.lenGrid):
                verticalArray.append(self.arrayField[lineInt][self.setRow])
            if verticalArray == checkArray:
                return 1
        
        # diagonal left_top to right_bottom check
        setLineNew = self.setLine
        setRowNew = self.setRow

        while setLineNew > 0 and setRowNew > 0:
            setLineNew -= 1
            setRowNew -= 1

        arrayDiagonal = []
        while setLineNew < self.lenGrid and setRowNew < self.lenGrid:
            arrayDiagonal.append(self.arrayField[setLineNew][setRowNew])
            setLineNew += 1
            setRowNew += 1

        for i in range(lenFor):
            if arrayDiagonal[i:self.endGameCount+i] == checkArray:
                return 1

        # diagonal right_top to left_bottom check

        setLineNew = self.setLine
        setRowNew = self.setRow

        while setLineNew > 0 and setRowNew < self.lenGrid-1:
            setLineNew -= 1
            setRowNew += 1

        arrayDiagonal = []
        while setLineNew < self.lenGrid and setRowNew > -1:
            arrayDiagonal.append(self.arrayField[setLineNew][setRowNew])
            setLineNew += 1
            setRowNew -= 1

        for i in range(lenFor):
            if arrayDiagonal[i:self.endGameCount+i] == checkArray:
                return 1


        # draw check
        countNul = 0
        for line in self.arrayField:
            for row in line:
                if row == " ":
                    countNul += 1
        if countNul == 0:
            return 2
        
        return 0

gm = Game()