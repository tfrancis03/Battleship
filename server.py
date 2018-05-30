#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    playerId = 0
    while True:
        # stop allowing new connections when two poeple have connected to server
        if(len(addresses) < 2):
            client, client_address = SERVER.accept()
            print("%s:%s has connected." % client_address)
            client.send(bytes(str(playerId), "utf8"))
            addresses[client] = client_address
            print(len(addresses))
            Thread(target=handle_client, args=(client,playerId,)).start()
            playerId += 1


def handle_client(client, id):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    clients[client] = name
    players[id] = name 
    welcome = 'Welcome player %d, %s! If you ever want to quit, type {quit} to exit.' % (id, name)
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))

    global turn
    while True:

        msg = "player %d \n turn" % turn
        broadcast(bytes(msg, "utf8"))
        msg = client.recv(BUFSIZ)

        if msg != bytes("{quit}", "utf8") and turn == id:
            broadcast(msg, name+": ")
            turn += 1
            turn %= 2
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
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