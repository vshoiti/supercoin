
def readPeers(arq, peerSet):
    with open(arq, "r") as peers:
        for line in peers:
            peerSet.add(line[:-1])

def writePeers(arq, peerSet):
    with open(arq, "w") as peers: 
        for peer in peerSet:
            peers.write('{}\n'.format(peer))

if __name__ == '__main__':
    peerSet = set() 
    readPeers("cpeers.txt", peerSet)
    print(peerSet)
    addPeer("cpeers.txt", "1234215")
    readPeers("cpeers.txt", peerSet)
    print(peerSet)

