from socket import *

serverName = "127.0.0.1" #coocar o ip do peer central
serverPort = 12000

initialSocket = socket(AF_INET, SOCK_STREAM)
initialSocket.connect((serverName, serverPort))
initialSocket.send("1".encode())


data = initialSocket.recv(1024).decode()
print(data)
with open("cpeers.txt", "w") as peers:
    peers.write(data)
initialSocket.close()