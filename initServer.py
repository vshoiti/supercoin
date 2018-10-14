from socket import *
from utils import *
import sys

SERVER = "127.0.0.1" #colocar o ip do peer central
PORT = 12000
BUFFER = 1024

initialSocket = socket(AF_INET, SOCK_STREAM)
initialSocket.connect((SERVER, PORT))
initialSocket.send("1".encode())

data = initialSocket.recv(BUFFER)
peersSet = eval(data.decode())
peersSet.add(SERVER)
writePeers("cpeers.txt", peersSet)

initialSocket.close()

