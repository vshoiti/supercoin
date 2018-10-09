from socket import *
from utils import *

peersSet = set()

serverName = "35.229.88.152" #colocar o ip do peer central
serverPort = 12000
peersSet.add(serverName)

initialSocket = socket(AF_INET, SOCK_STREAM)
initialSocket.connect((serverName, serverPort))
initialSocket.send("1".encode())


data = initialSocket.recv(1024).decode()
print(data)
with open("cpeers.txt", "w") as peers:
    peers.write(data)
initialSocket.close()

print(peersSet)
readPeers("cpeers.txt", peersSet)
print(peersSet)