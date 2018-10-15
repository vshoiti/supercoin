from utils import *
from Block import Block
from socket import *

import threading
import _thread


# TODO: finish mining and messaging

HOST = ''
# PORT = 12002


class Miner(threading.Thread):
    def __init__(self, node, prev_hash, index, transactions):
        # adaptado de: https://stackoverflow.com/a/325528
        super(Miner, self).__init__()
        self._stop_event = threading.Event()

        self.node = node
        self.address = node.address
        self.prev_hash = prev_hash
        self.difficulty = node.difficulty
        self.index = index
        self.peers = node.peers

        self.block = Block(self.index, self.prev_hash)
        self.block.transactions.append({self.address: 10})
        for transaction in transactions:
            self.block.transactions.append(transaction)

    # adaptado de: https://stackoverflow.com/a/325528
    def stop(self):
        self._stop_event.set()

    # adaptado de: https://stackoverflow.com/a/325528
    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        return self.mine()

    def mine(self):
        while not self.stopped():
            if len(self.block.transactions) > 1:
                block_hash = hash_string(str(self.block))

                if self.verify_difficulty(block_hash):
                    return self.propagate_block()

                self.block.nonce += 1

    def propagate_block(self):
        self.node.add_new_blocks([self.block], self.index)

        for peer in self.node.peers:
            peer = eval(str(peer))
            _thread.start_new_thread(self.send_block, (peer[0], peer[1]))

        return

    def send_block(self, peer_ip, peer_port):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((peer_ip, peer_port))
        s.send(write_message('new_block', self.block))

    def verify_difficulty(self, block_hash):
        first_chars = block_hash[:self.difficulty]
        first_chars = first_chars.replace('0', '')  # remove os zeros
        if first_chars:
            return False  # first_chars não está vazia
        return True
