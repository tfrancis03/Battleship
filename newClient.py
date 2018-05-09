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
        self.myBoard = Canvas(root, width=200, height=200)
        self.myBoard.grid(row=3, column=0)

        # Board object for Enemey
        self.enemyBoard = Canvas(root, width=200, height=200)
        self.enemyBoard.grid(row=3, column=1)

        # Input Boxes for Player
        self.moveInput = Entry(root).grid(row=4, column=0, columnspan=2)
        self.submitMove = Button(root, text="Submit Move").grid(
            row=5, column=0, columnspan=2)

        # draw player boards
        self.drawBoards()

    def drawBoards(self):
        self.drawSelf()
        self.drawEnemy()

    def drawEnemy(self):
        for row in range(19):
            for column in range(10):
                size = 20
                self.enemyBoard.create_rectangle(size * column,
                                                 size * row,
                                                 size * (column + 1),
                                                 size * (row + 1),
                                                 fill='dark blue')

    def drawSelf(self):
        for row in range(19):
            for column in range(10):
                size = 20
                self.myBoard.create_rectangle(size * column,
                                              size * row,
                                              size * (column + 1),
                                              size * (row + 1),
                                              fill='light blue')


root = Tk()
root.geometry("400x300+300+300")
style = ttk.Style()
style.theme_use('classic')
root.title('Battleship')

app = Main(root)
root.mainloop()
