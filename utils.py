
def readPeers(arq, peerSet):
    with open(arq, "r") as peers:
        for line in peers:
            print(line[:-1])
            peerSet.add(line[:-1])
            
def addPeer(arq, ip):
    with open(arq, "a") as peers:
        peers.write('{}\n'.format(ip))


if __name__ == '__main__':
    peerSet = set() 
    readPeers("cpeers.txt", peerSet)
    print(peerSet)
    addPeer("cpeers.txt", "1234215")
    readPeers("cpeers.txt", peerSet)
    print(peerSet)

