from socket import *

file = open("peers.txt", "w+")
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
            peers.write(f'{addr[0]}\n')
        with open("peers.txt", "r") as peers:
            connectionSocket.send(peers.read().encode())
    connectionSocket.close()
