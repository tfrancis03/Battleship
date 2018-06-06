#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from enum import Enum     # for enum34, or the stdlib version
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json
from pprint import pprint

class InputState(Enum):
    Coordinates = 1
    Orientation = 2

class GameState(Enum):
    Build = 1
    Battle = 2
    Connect = 3
    Ready = 4
    GameOver = 5

class Main:

    def __init__(self, master):
        # sets the window frame object
        self.frame = Frame(master)
        
        #Player ID
        self.playerId = -1 

        # Labels for the screen
        self.welcomeLabel = Label(root, text="Welcome to Battleship!").grid(
            row=0, column=0, columnspan=2)

        # Set Top Message
        self.topMessage = StringVar()
        self.turnLabel = Label(root, textvariable=self.topMessage).grid(
            row=1, column=0, columnspan=2)
        self.topMessage.set("Player " + str(self.playerId))

        self.myLabel = Label(root, text="Your Board").grid(
            row=2, column=0, sticky=W+E)
        self.enemyLabel = Label(root, text="Enemy Board").grid(
            row=2, column=1, sticky=W+E)

        # Client States
        self.inputState = InputState.Coordinates
        self.gameState = GameState.Connect

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
        self.moveInput.bind('<Return>',lambda event: self.insertMove())
        self.message.set("Please enter coordinates (ex: 3a,A6,5A)")
        self.moveInput.grid(row=5, column=0, columnspan=2)

        self.submitMove = Button(root, text="Submit Move", command=self.insertMove).grid(
            row=6, column=0, columnspan=2)
        
        # Is player's turn
        self.isTurn = True

        # draw player boards
        self.drawBoards()

        # storing the players board
        self.myBoard = [[-1 for x in range(10)] for y in range(10)]
        self.enemyBoard = [[-1 for x in range(10)] for y in range(10)]
        self.client_socket = None
        self.receive_thread = None

        # SHIPS
        self.shipList = {"Aircraft Carrier": 5,
             "Battleship": 4,
             "Submarine": 3,
             "Destroyer": 3,
             "Patrol Boat": 2}
        self.shipInventory = ["Aircraft Carrier","Battleship","Submarine","Destroyer","Patrol Boat"]

    def connectToServer(self, host, port):
        addr = (host, port)
        # Start Client Socket
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(addr)

        # Start the Thread for the Sever Messages
        self.receive_thread = Thread(target=self.messagesFromServer)
        self.receive_thread.start()

    def messagesFromServer(self):
        BUFSIZ = 1024
        while True:
            try:
                msg = self.client_socket.recv(BUFSIZ).decode("utf8")
                pprint(msg)
                json_data = json.loads(msg)
                pprint(json_data)
                self.handleMessageFromServer(json_data)
            except OSError:  # Possibly client has left the chat.
                break

    def handleMessageFromServer(self, data):
        
        if("message" in data):
            msg = data["message"]
            self.message.set(msg)
            if("begin" in msg):
                self.gameState = GameState.Battle

        if(self.gameState == GameState.Connect):
            self.playerId = int(data["playerId"])+1
            self.topMessage.set("Player " + str(self.playerId))
            self.gameState = GameState.Ready

    def sendToServer(self):
        data = {}
        data["playerId"] = self.playerId
        data["myBoard"] = self.myBoard
        data["enemyBoard"] = self.enemyBoard
        data["attackCords"] = self.cord
        data["message"] = "MESSAGE"
        data["gameState"] = self.gameState.name
        json_data = json.dumps(data)
        self.client_socket.send(bytes(str(json_data), "utf8"))
        #print(json_data)

    def destroy(self):
        self.client_socket.shutdown(1)
        self.client_socket.close()

    def insertMove(self):
        entry = self.moveInput.get()
        #print(entry)
        #NEXT TIME TODO: Pass in current ship into self.validate on line 81
        
        if(self.gameState == GameState.Build and self.inputState == InputState.Coordinates):
            self.cord = self.getCord(entry)
                
            if(self.cord[0] != -1): 
                self.message.set("Select the orientation of the ship (v, h)")
                self.inputState = InputState.Orientation
            else:
                self.message.set("Invalid move.")
            
        elif(self.gameState == GameState.Build and self.inputState == InputState.Orientation):
                if self.validate(entry):
                    self.myBoard = self.place_ship(entry)
                    self.updateMyBoard(self.myBoard)
                    self.inputState = InputState.Coordinates
                    self.message.set("Please enter coordinates (ex: 3a,A6,5A)")

                if(len(self.shipInventory) < 1):
                    self.message.set("BATTLE TIME! ENTER THOSE COORDINATES!")
                    self.gameState = GameState.Battle
                    self.inputState = InputState.Coordinates

        # Elsewhere would change state from build to battle
        elif self.gameState == GameState.Battle: # Battle State
            self.cord = self.getCord(entry)
            if self.isTurn:
                self.sendToServer()
                #result = self.user_attack_phase()
                #self.updateEnemyBoard
                #self.message.set("Be warned: Incoming enemy artillery")
            else:
                self.message.set("Oh, come on. It's not your turn.")
        
        elif (self.gameState == GameState.Ready):
            self.sendToServer()

        self.moveInput.delete(0, 'end')

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

    def place_ship(self, ori):
        r = self.cord[0]
        c = self.cord[1]
        length = self.shipList[self.shipInventory[0]]
        # place ship based on orientation
        if ori == "v":
            for i in range(length):
                self.myBoard[r+i][c] = self.shipInventory[0][0]
        elif ori == "h":
            for i in range(length):
                self.myBoard[r][c+i] = self.shipInventory[0][0]

        self.shipInventory.pop(0)
        return self.myBoard

    def drawBoardGuide(self):
        for i in range(10):
            val = ord('a')
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
                tile = piece
                if(piece == -1):
                    tile = "~"
                self.myCanvas.create_text(
                    20*ci + 26, 20*ri + 23, anchor=NW,
                    font="Purisa", text=tile)

    def updateEnemyBoard(self, board):
        self.drawEnemy()
        self.drawBoardGuide()
        for ri, row in enumerate(board):
            for ci, piece in enumerate(row):
                tile = piece
                if(piece == -1):
                    tile = "~"
                self.enemyCanvas.create_text(
                    20*ci + 26, 20*ri + 23, anchor=NW,
                    font="Purisa", text=tile)
    
    def check_sink(self, board):
        # figure out what ship was hit
        x = self.cord[0]
        y = self.cord[1]
        if board[x][y] == "A":
            ship = "Aircraft Carrier"
        elif board[x][y] == "B":
            ship = "Battleship"
        elif board[x][y] == "S":
            ship = "Submarine"
        elif board[x][y] == "D":
            ship = "Destroyer"
        elif board[x][y] == "P":
            ship = "Patrol Boat"

        # mark cell as hit and check if sunk
        board[-1][ship] -= 1
        if board[-1][ship] == 0:
            print(ship + " Sunk")

    def attempt_attack(self):
        board = self.enemyBoard
        x = self.cord[0]
        y = self.cord[1]
        # make a move on the board and return the result, hit, miss or try again for repeat hit
        if board[x][y] == -1:
            return "miss"
        elif board[x][y] == '*' or board[x][y] == '$':
            return "try again"
        else:
            return "hit"

    def user_attack_phase(self):
        
        # get coordinates from the user and try to make move
        # if move is a hit, check ship sunk and win condition
        board = self.enemyBoard
        x = self.cord[0]
        y = self.cord[1]
        res = self.attempt_attack()
        if res == "hit":
            print("Hit at " + str(x+1) + "," + str(y+1))
            check_sink(board, x, y)
            board[x][y] = '$'
            if check_win(board):
                self.message.set("Victory! Victory! Victory!")
                return "WIN"
            else:
                print("Enemy turn")
        elif res == "miss":
            print("Sorry, " + str(x+1) + "," + str(y+1) + " is a miss.")
            print("Enemy turn")
            self.message.set("Ya missed, bud. Now it's the enemy's turn.")
            board[x][y] = "*"
        elif res == "try again":
            print("Sorry, that coordinate was already hit. Please try again")
            self.message.set("Here's an idea, don't hit the same spot twice. Try again.")
            self.user_attack_phase()

        if res != "try again":
            return board

    def validate(self, ori):
        if len(self.shipInventory) > 0:
            r = self.cord[0]
            c = self.cord[1]
            length = self.shipList[self.shipInventory[0]]
            if ori == "v" and r+length > 10:
                return False
            elif ori == "h" and c+length > 10:
                return False
            else:
                if ori == "v":
                    for i in range(length):
                        if self.myBoard[r+i][c] != -1:
                            return False
                elif ori == "h":
                    for i in range(length):
                        if self.myBoard[r][c+i] != -1:
                            return False
                
        return True

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

    def testBoard(self):
        row = 0
        col = 0
        while(len(self.shipInventory) > 0):
            self.cord = [row, col]
            self.place_ship('v')
            col += 1
        self.gameState = GameState.Connect
        self.message.set("Press Submit Move to Send Board to Server")

root = Tk()
root.geometry("450x400+300+300")
style = ttk.Style()
style.theme_use('alt')
root.title('Battleship')

# Start Main Class
app = Main(root)
app.testBoard()
app.updateMyBoard(app.myBoard)
app.updateEnemyBoard(app.enemyBoard)

# Connect to Server
ipAddress = ''
app.connectToServer(ipAddress , 5000)
root.mainloop()
root.protocol("WM_DELETE_WINDOW", app.destroy)