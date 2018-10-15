#!/usr/bin/python3.5

from socket import *
from utils import *
import _thread


def sendPeers(connection_socket):
    try:
        msg = ''
        while True:
            data = connection_socket.recv(1024).decode('ascii')
            if not data:
                break
            msg += data

        code, data = read_message(msg)
        if code == 'connect':
            peers = repr(peersSet)
            connection_socket.send(write_message('ok', peers))

            if (addr[0], data) not in peersSet:
                peersSet.add((addr[0], data))
                # with open("peers.txt", "a") as peers:
                #     peers.write("{}\n".format((addr[0], data)))
        connection_socket.close()
    finally:
        connection_socket.close()


peersSet = set()
# readPeers("peers.txt", peersSet)
# print(peersSet)

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready")

while 1:
    connectionSocket, addr = serverSocket.accept()
    thread = _thread.start_new_thread(sendPeers, (connectionSocket,))
