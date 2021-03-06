#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys
import json
from pprint import pprint

class Game:
    def __init__(self):
        self.playerBoard = {} #map playerId to board
        self.playerShips = {} # playerId -> ships -> shipCounts
        self.ready = [False, False]
        self.numPlayer = 2
        self.turn = 0

    def changeTurn(self):
        self.turn += 1
        self.turn %= 2

    def getPlayer(self, i):
        return self.playerBoard[i]

    def getEnemy(self, i):
        if(i == 1):
            return self.playerBoard[2]
        return self.playerBoard[1]

    def validMove(self, playerId, move):
        enemy = self.getEnemy(playerId)
        tile = enemy[move[0]][move[1]]
        if(tile == "$" or tile == "*"):
            return False
        return True

    def isHit(self, playerId, move):
        enemy = self.getEnemy(playerId)
        tile = enemy[move[0]][move[1]]
        if(tile == -1): #hit has occured
            enemy[move[0]][move[1]] = "*" 
            return tile
        # decrement ship count for the player
        self.playerShips[playerId][tile] -= 1
        enemy[move[0]][move[1]] = "$" 
        return tile

    def checkSink(self, playerId, tile):
        count = self.playerShips[playerId][tile]
        if(count <= 0):
            return True
        return False

    def parseShips(self, playerId):
        print("Parsing ships..")
        board = self.playerBoard[playerId]
        self.playerShips[playerId] = {}
        for row in board:
            for piece in row:
                # is piece in dictionary
                if(piece not in self.playerShips[playerId]):
                    self.playerShips[playerId][piece] = 1
                    continue
                # increment piece count
                self.playerShips[playerId][piece] += 1
        print("Parsed Ships")
        pprint(self.playerShips)

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    playerId = 0
    while True:
        # stop allowing new connections when two poeple have connected to server
        if(len(addresses) < 2):
            client, client_address = SERVER.accept()
            print("%s:%s has connected." % client_address)
            data = {}
            data["playerId"] = playerId
            json_data = json.dumps(data)
            client.send(bytes(str(json_data), "utf8"))
            addresses[client] = client_address
            print(len(addresses))
            Thread(target=handle_client, args=(client,playerId,)).start()
            playerId += 1

# Process moves from Sever
def gameLogic(data):
    global game
    # reading info from client
    state = data["gameState"]
    playerId = data["playerId"]
    move = data["attackCords"]
    player = data["myBoard"]

    sendBack = {}
    if(state == "Ready"): #Set Each Player
        game.playerBoard[playerId] = player #set the current player board
        game.parseShips(playerId)
        #game.ready[playerId-1] = True # player n is ready to start
        if(1 in game.playerBoard and 2 in game.playerBoard):
            sendBack["message"] = "Let the battle begin! Player 1's Turn"
            game.turn = 0
        else:
            sendBack["message"] = "Both players are not ready to start"

    elif(state == "Battle"):
        if(playerId != game.turn+1): #Prevent Other Player from Entering Move 
            # Not Your Turn 
            sendBack["message"] = "Not your turn %d" % playerId
            clients[playerId-1].send(jsonToBytes(json.dumps(sendBack))) #only send message to person who's not turn it is
            return
        else: # Is it your turn
            # game logic
            # determine if move is new
            if(not game.validMove(playerId, move)):
                sendBack["message"] = "Not a valid move"
                clients[playerId-1].send(jsonToBytes(json.dumps(sendBack)))
                return
            # determine hit or miss
            # TODO: check when a ship is sunk
            tile = game.isHit(playerId, move)
            if( tile != -1): #will also update enemy board
                sendBack["message"] = "Player %d hit " % playerId
                if(game.checkSink(playerId, tile)):
                    sendBack["message"] += "and sunk %s " % tile
            else:
                sendBack["message"] = "Player %d misses. " % playerId
            sendBack["enemyBoard"] = game.getPlayer(playerId)
            sendBack["myBoard"] = game.getEnemy(playerId)
            game.changeTurn()
            sendBack["message"] += "Player %d's turn." % (game.turn+1)

    sendBack["playerId"] = game.turn + 1
    sendBack = json.dumps(sendBack)
    pprint(sendBack)
    broadcast(jsonToBytes(sendBack))

# $ hit, * miss

def jsonToBytes(json_data):
    return bytes(str(json_data), "utf8")

def handle_client(client, id):  # Takes client socket as argument.
    """Handles a single client connection."""
    global turn
    clients[id] = client
    while True:

        msg = client.recv(BUFSIZ).decode("utf8")
        data = json.loads(msg)
        pprint(data)
        if msg != bytes("{quit}", "utf8"):
            gameLogic(data)
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            break

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    global clients
    for sock in clients.values():
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}
players = {}
turn = 0

HOST = ''
PORT = 5000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
game = Game()

if __name__ == "__main__":
    try:
        SERVER.listen(5)
        print("Waiting for connection...")
        ACCEPT_THREAD = Thread(target=accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()
    except KeyboardInterrupt:
        print("keyboard interrupt")
        ACCEPT_THREAD.join()
        SERVER.close()
        sys.exit()    

'''
1. Get Connections from two clients
- assign id to each client
2. Get an ACK from each client once setup is done
- Get a copy of each player's board
3. Enter Battle State 
- Alternate inputs between clients
- Get a coord move
- Validate Move
- Attack Other Player
- Send Boards to Clients
- Check if a win state has occured
4. Win State
'''