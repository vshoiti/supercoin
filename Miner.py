from utils import *
from Block import Block

import threading
import _thread
import socket


# TODO: get state? finish mining and messaging

HOST = ''
PORT = 12021


class Miner(threading.Thread):
    def __init__(self, node, prev_hash, index):
        # adaptado de: https://stackoverflow.com/a/325528
        super(Miner, self).__init__()
        self._stop_event = threading.Event()

        self.address = node.address
        self.prev_hash = prev_hash
        self.difficulty = node.difficulty
        self.index = index
        self.state = node.current_state
        self.peers = node.peers

        self.block = Block(self.index, self.prev_hash)

    # adaptado de: https://stackoverflow.com/a/325528
    def stop(self):
        self._stop_event.set()

    # adaptado de: https://stackoverflow.com/a/325528
    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        return self.mine()

    def mine(self):
        self.block.transactions.append({self.address: 10})

        _thread.start_new_thread(self.listen_transactions, ())

        while not self.stopped():
            if len(self.block.transactions) > 1:
                block_hash = hash_string(str(self.block))

                if self.verify_difficulty(block_hash):
                    return self.propagate_block()

                self.block.nonce += 1

    def listen_transactions(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.listen()
        while True:
            peer_socket, address = s.accept()
            _thread.start_new_thread(self.receive_transaction, (peer_socket, address))
        s.close()

    def receive_transaction(self, peer_socket, address):
        msg = ""
        while True:
            data = peer_socket.recv(1024)
            msg += data
            if not data:
                break
        code, data = read_message(msg)
        if code != 'transaction':
            peer_socket.send(write_message('?', None))
        elif len(self.block.transactions) >= 10:
            peer_socket.send(write_message('full_block', None))
        elif self.accept_transaction(data):
            peer_socket.send(write_message('tr_accepted'))
        peer_socket.close()

    def accept_transaction(self, transaction):
        candidate_state = self.state.copy()

        if sum(transaction.values()) != 0:
            return False

        for address in transaction.keys():
            if address in candidate_state.keys():  # o endereço existe
                if candidate_state[address] - transaction[address] >= 0:  # o endereço possue fundos suficientes
                    candidate_state[address] += transaction[address]
                else:
                    return False
            # se o endereço não existe mas a quantia é positiva
            elif transaction[address] > 0:
                # cria o endereço
                candidate_state[address] = transaction[address]
            else:  # a quantia é negativa
                return False

        self.block.transactions.append(transaction)
        self.state = candidate_state
        return True

    def propagate_block(self):
        print(self.block.nonce)
        print(self.block.transactions)
        print((self.block.__str__()))
        return  # TODO

    def verify_difficulty(self, block_hash):
        first_chars = block_hash[:self.difficulty]
        first_chars = first_chars.replace('0', '')  # remove os zeros
        if first_chars:
            return False  # first_chars não está vazia
        return True
