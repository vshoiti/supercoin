#!/usr/bin/python3.5

from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready")

while 1:
    connectionSocket, addr = serverSocket.accept()
    code = connectionSocket.recv(1024)
    if code.decode() == "1":
        with open("peers.txt", "a") as peers:
            peers.write('{}\n'.format(addr[0]))
        with open("peers.txt", "r") as peers:
            connectionSocket.send(peers.read().encode())
    connectionSocket.close()
