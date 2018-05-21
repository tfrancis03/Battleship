#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from enum import Enum     # for enum34, or the stdlib version

class InputState(Enum):
    Coordinates = 1
    Orientation = 2

class GameState(Enum):
    Build = 1
    Battle = 2

class Main:

    def __init__(self, master):
        # sets the window frame object
        self.frame = Frame(master)

        # Labels for the screen
        self.welcomeLabel = Label(root, text="Welcome to Battleship!").grid(
            row=0, column=0, columnspan=2)
        self.turnLabel = Label(root, text="Player X's Turn").grid(
            row=1, column=0, columnspan=2)
        self.myLabel = Label(root, text="Your Board").grid(
            row=2, column=0, sticky=W+E)
        self.enemyLabel = Label(root, text="Enemy Board").grid(
            row=2, column=1, sticky=W+E)

        # Client States
        self.inputState = InputState.Coordinates
        self.gameState = GameState.Build

        # Board object for Player
        self.myCanvas = Canvas(root, width=220, height=220)
        self.myCanvas.grid(row=3, column=0)

        # Board object for Enemey
        self.enemyCanvas = Canvas(root, width=220, height=220)
        self.enemyCanvas.grid(row=3, column=1)

        # Input Boxes for Player
        self.message = StringVar()
        self.messageLabel = Label(textvariable=self.message).grid(
            row=4, column=0, columnspan=2)
        self.moveInput = Entry(root)
        self.message.set("Please enter coordinates (ex: 3a,A6,5A)")
        self.moveInput.grid(row=5, column=0, columnspan=2)

        self.submitMove = Button(root, text="Submit Move", command=self.insertMove).grid(
            row=6, column=0, columnspan=2)

        # draw player boards
        self.drawBoards()

        # storing the players board
        self.myBoard = [[-1 for x in range(10)] for y in range(10)]
        self.enemyBoard = [[-1 for x in range(10)] for y in range(10)]

    def insertMove(self):
        entry = self.moveInput.get()
        print(entry)

        if(self.gameState == GameState.Build and self.inputState == InputState.Coordinates):
            cord = self.getCord(entry)
            if(cord[0] != -1): 
                self.message.set("Select the orientation of the ship (v, h)")
                self.inputState = InputState.Orientation
            else:
                self.message.set("Invalid move.")
            
        elif(self.gameState == GameState.Build and self.inputState == InputState.Orientation):
            oren = self.getOrientation(entry)

        # Elsewhere would change state from build to battle
        else: # Battle State
            cord = self.getCord(entry)
    
    def drawBoards(self):
        self.drawSelf()
        self.drawEnemy()
        self.drawBoardGuide()

    def drawEnemy(self):
        for row in range(11):
            for column in range(11):
                size = 20
                self.enemyCanvas.create_rectangle(size * column,
                                                 size * row,
                                                 size * (column + 1),
                                                 size * (row + 1),
                                                 fill='blue')

    def drawSelf(self):
        for row in range(11):
            for column in range(11):
                size = 20
                #self.myCanvas.create_text(20, 30, anchor=W, font="Purisa",
                #    text="A")
                self.myCanvas.create_rectangle(size * column,
                                              size * row,
                                              size * (column + 1),
                                              size * (row + 1),
                                              fill='light blue')

    def drawBoardGuide(self):
        for i in range(10):
            val = ord('A')
            self.myCanvas.create_text(7, 20*i + 30, anchor=W, font="Purisa",
                text=chr(val+i))
            self.myCanvas.create_text(20*i + 25, 10, anchor=W, font="Purisa",
                text=i+1)

            self.enemyCanvas.create_text(7, 20*i + 30, anchor=W, font="Purisa",
                text=chr(val+i))
            self.enemyCanvas.create_text(20*i + 25, 10, anchor=W, font="Purisa",
                text=i+1)

    def updateMyBoard(self, board):
        self.drawSelf()
        self.drawBoardGuide()
        for ri, row in enumerate(board):
            for ci, piece in enumerate(row):
                self.myCanvas.create_text(
                    20*ci + 26, 20*ri + 23, anchor=NW,
                    font="Purisa", text=piece)

    def updateEnemyBoard(self, board):
        self.drawEnemy()
        self.drawBoardGuide()
        for ri, row in enumerate(board):
            for ci, piece in enumerate(row):
                self.myCanvas.create_text(
                    20*ci + 26, 20*ri + 23, anchor=NW,
                    font="Purisa", text=piece)
    
    def getOrientation(self, oren):
        pass

    def getCord(self, user_input):

        while (True):
                OriginalCoor = list(user_input)
                coor = ['0', '0']
                #print(OriginalCoor)

                if len(OriginalCoor) > 3:
                    raise Exception("Invalid entry, too few/many coordinates.")

                # check that 2 values are integers
                num = -1
                alpha = -1
                firstNum = True
                for i, c in enumerate(OriginalCoor):
                    if c.isalpha():
                        if c.isupper():
                            alpha = ord(c)-ord('A')
                        else:
                            alpha = ord(c)-ord('a')
                    else:
                        if(firstNum and len(OriginalCoor) == 3):
                            s = int(c + OriginalCoor[i+1])
                            firstNum = False
                            if(s <= 10):
                                num = s - 1
                        if(len(OriginalCoor)==2):
                            num = int(c) - 1
                
                coor[0] = alpha
                coor[1] = num

                # check that values of integers are between 1 and 10 for both coordinates
                if coor[0] > 9 or coor[0] < 0 or coor[1] > 9 or coor[1] < 0:
                    print(
                        "Invalid entry. Please use values between 1 to 10 and A to J or a to j only.")

                # if everything is ok, return coordinates
                print(coor)
                return coor

root = Tk()
root.geometry("450x400+300+300")
style = ttk.Style()
style.theme_use('alt')
root.title('Battleship')

app = Main(root)
board = [['a','b','c','x'],['d','e','f'],['g','h','i']]
#app.updateMyBoard(board)
root.mainloop()
