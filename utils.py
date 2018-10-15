from Crypto.Hash import SHA256


def read_message(msg):
    code, data = msg.split('=')
    data = rebuild_data(data)

    return code, data


def write_message(code, data):
    return (code + '=' + build_data(data)).encode('ascii')


def build_data(data):
    return str(data)


def rebuild_data(data):
    return eval(data)


def readPeers(arq, peerSet):
    with open(arq, "r") as peers:
        for line in peers:
            peerSet.add(line[:-1])


def writePeers(arq, peerSet):
    with open(arq, "w") as peers: 
        for peer in peerSet:
            peers.write('{}\n'.format(peer))


def hash_string(string):
    string = string.encode('utf-8')
    return SHA256.new(string).hexdigest()


if __name__ == '__main__':
    peerSet = set() 
    readPeers("cpeers.txt", peerSet)
    print(peerSet)
    addPeer("cpeers.txt", "1234215")
    readPeers("cpeers.txt", peerSet)
    print(peerSet)

