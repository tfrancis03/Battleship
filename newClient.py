#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk


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

        # Board object for Player
        self.myCanvas = Canvas(root, width=220, height=220)
        self.myCanvas.grid(row=3, column=0)

        # Board object for Enemey
        self.enemyCanvas = Canvas(root, width=220, height=220)
        self.enemyCanvas.grid(row=3, column=1)

        # Input Boxes for Player
        self.moveInput = Entry(root).grid(row=4, column=0, columnspan=2)
        self.submitMove = Button(root, text="Submit Move").grid(
            row=5, column=0, columnspan=2)

        # draw player boards
        self.drawBoards()

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
        pass

    def updateEnemyBoard(self, board):
        pass

root = Tk()
root.geometry("450x350+300+300")
style = ttk.Style()
style.theme_use('alt')
root.title('Battleship')

app = Main(root)
root.mainloop()
