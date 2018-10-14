#!/usr/bin/python3.5

from socket import *
from utils import *
from threading import *

peersSet = set()

readPeers("peers.txt", peersSet)

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready")

def sendPeers(connectionSocket):
    code = connectionSocket.recv(1024)
    if code.decode() == "1":
        connectionSocket.send(repr(peersSet).encode())
        addrSet = {addr[0]}    
        if not peersSet.issuperset(addrSet):
            with open("peers.txt", "a") as peers:
                peers.write('{}\n'.format(addr[0]))
        peersSet.add(addr[0])

while 1:
    connectionSocket, addr = serverSocket.accept()
    thread = Thread(target=sendPeers, args=(connectionSocket,))
    thread.start()

connectionSocket.close()
