from socket import *
from utils import *

peersSet = set()
serverName = "127.0.0.1" #colocar o ip do peer central
serverPort = 12000
peersSet.add(serverName)

initialSocket = socket(AF_INET, SOCK_STREAM)
initialSocket.connect((serverName, serverPort))
initialSocket.send("1".encode())

data = initialSocket.recv(1024)
print(eval(data.decode()))
peersSet = eval(data.decode())
writePeers("cpeers.txt", peersSet)

initialSocket.close()

