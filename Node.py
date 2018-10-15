from Genesis import Genesis
from Blockchain import Blockchain
from Miner import Miner
from Block import Block

from utils import *
from socket import *
from threading import RLock
import _thread

SERVER = 'localhost'  # colocar o ip do peer central
SERVER_PORT = 12000
BUFFER = 1024


class Node:

    def __init__(self, address, own_port):
        self.address = address  # wallet address
        self.own_port = own_port  # porta na qual receberá requests
        self.peers = None
        self.blockchain = Blockchain(Genesis())
        self.difficulty = 4
        self.current_state = None
        self.miner = None
        self.transaction_pool = []
        self.lock = RLock()

    def start_node(self):
        initial_socket = socket(AF_INET, SOCK_STREAM)
        initial_socket.connect((SERVER, SERVER_PORT))
        initial_socket.send(write_message('connect', self.own_port))
        initial_socket.shutdown(SHUT_WR)

        try:
            response = ''
            while True:
                data = initial_socket.recv(1024).decode('ascii')
                if not data:
                    break
                response += data
            print(response)
            code, data = read_message(response)
            if code == 'ok':
                self.peers = eval(str(data))
                writePeers("cpeers.txt", self.peers)
        finally:
            initial_socket.close()

        for peer in self.peers:
            peer = eval(str(peer))
            self.request_top_block(peer_ip=peer[0], peer_port=peer[1])
        self.listen_requests()

    def request_top_block(self, peer_ip, peer_port):
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((peer_ip, peer_port))
            s.send(write_message('get_top', None))
            s.shutdown(SHUT_WR)

            response = ''
            while True:
                data = s.recv(BUFFER).decode('ascii')
                if not data:
                    break
                response += data
            code, data = read_message(response)
            if code == 'top_block':
                block = rebuild_block(data)
                self.receive_block(block, peer_ip, peer_port)

        except ConnectionRefusedError:
            # self.peers.remove((peer_ip, peer_port))
            print(peer_ip, ':', peer_port, ' is unreachable')

    def receive_block(self, new_block, sender_ip, sender_port):
        last_block = self.blockchain.get_last()

        if new_block.index <= last_block.index:
            return False  # stale block

        else:
            # verifica o novo bloco e a chain a qual pertence, se diferente da atual
            self.validate_chain(new_block, sender_ip, sender_port)

    def request_block(self, block_hash, sender_ip, sender_port):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((sender_ip, sender_port))
        s.send(write_message('get_block', block_hash))
        s.shutdown(SHUT_WR)

        response = ''
        while True:
            data = s.recv(BUFFER).decode('ascii')
            if not data:
                break
            response += data
        code, data = read_message(response)
        if code == 'block':
            block = rebuild_block(data)
            return block
        return None

    def listen_requests(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(('', self.own_port))
        s.listen()

        while 1:
            conn, addr = s.accept()
            _thread.start_new_thread(self.route_request, (conn, addr))

    def send_transactions(self, receiving_address, ammount):
        for peer in self.peers:
            peer = eval(str(peer))
            _thread.start_new_thread(self.send_transaction, (peer[0], peer[1], receiving_address, ammount))

    def send_transaction(self, peer_ip, peer_port, receiving_address, amount):
        data = {self.address: -amount, receiving_address: amount}
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((peer_ip, peer_port))
            s.send(write_message('transaction', data))
            s.shutdown(SHUT_WR)

            response = ''
            while True:
                data = s.recv(BUFFER).decode('ascii')
                if not data:
                    break
                response += data
            code, data = read_message(response)
            print(peer_ip, ':', peer_port, ' - ', code)

        except ConnectionRefusedError:
            print(peer_ip, ':', peer_port, ' is unreachable')

    def receive_transaction(self, peer_socket, transaction):
        if not self.miner:
            peer_socket.send(write_message('not_mining', None))
        elif len(self.transaction_pool) >= 9:
            peer_socket.send(write_message('full_block', None))
        elif self.accept_transaction(transaction):
            peer_socket.send(write_message('tr_accepted', None))
        peer_socket.close()

    def route_request(self, conn, addr):
        msg = ''
        while 1:
            data = conn.recv(BUFFER).decode('ascii')
            if not data:
                break
            msg += data
        code, data = read_message(msg)
        if code == 'get_block':
            block_hash = data
            data = self.blockchain.get_block(block_hash)
            conn.send(write_message('block', data))
        elif code == 'get_top':
            data = self.blockchain.get_last()
            conn.send(write_message('top_block', data))
        elif code == 'new_block':
            block = rebuild_block(data)
            self.receive_block(block, sender_ip=addr[0], sender_port=addr[1])
        elif code == 'transaction':
            self.receive_transaction(conn, data)
        conn.close()

    def accept_transaction(self, transaction):
        candidate_state = self.get_current_state().copy()

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

        self.transaction_pool.append(transaction)
        self.restart_miner()
        return True

    def start_miner(self):
        prev_hash = hash_string(str(self.blockchain.get_last()))
        self.miner = Miner(self, prev_hash, self.blockchain.get_size(), self.transaction_pool)
        self.miner.start()

    def restart_miner(self):
        if self.miner:
            self.stop_miner()
            self.start_miner()

    def stop_miner(self):
        self.miner.stop()

    def get_current_state(self):
        if not self.current_state:
            return self.rebuild_current_state()
        return self.current_state

    # retorna um dict com todos os addresses existentes e seus fundos
    def rebuild_current_state(self):
        state = {}
        for transaction in self.blockchain.get_all_transactions():
            for address in transaction.keys():
                if address in state.keys():
                    state[address] += transaction[address]
                else:
                    state[address] = transaction[address]
        self.current_state = state
        return state

    def validate_chain(self, top_block, sender_ip, sender_port):
        self.lock.acquire()  # locka a blockchain para que ela não seja alterada durante a verificação
        try:
            different_blocks = [top_block]
            top_index = top_block.index

            current_block = top_block
            # itera para encontrar blocos diferentes dos quais a blockchain atual armazena
            while self.blockchain.get_block(current_block.prev_hash) is None:
                # pede o bloco diferente
                current_block = self.request_block(current_block.prev_hash, sender_ip, sender_port)
                top_index = current_block.index
                different_blocks.append(current_block)

            # itera sobre os blocos diferentes
            for block in different_blocks:
                if not self.validate_block(block):  # se o bloco não é valido
                    if top_index <= self.blockchain.get_size():  # e o tamanho da chain recebida é menor que a atual
                        return  # não faz nada
                    else:  # a chain nova é maior e correta até certo ponto
                        break  # adiciona
                else:  # o bloco é válido
                    top_index = block.index

            self.add_new_blocks(different_blocks, top_index)  # adiciona os novos blocos até o maior índice válido
        finally:
            self.lock.release()

    def validate_block(self, block):
        block_hash = hash_string(str(block))
        if not verify_size(block):
            return False
        if not self.verify_difficulty(block_hash):
            return False
        if not self.verify_transactions(block):
            return False

        print(block_hash, " accepted as valid")
        return True

    def add_new_blocks(self, blocks, top_index):
        self.current_state = None  # inutiliza a referencia atual do estado
        self.transaction_pool = []
        self.restart_miner()

        for block in blocks:
            if block.index <= top_index:
                self.blockchain.add_block(block, block.index)

    def verify_difficulty(self, block_hash):
        first_chars = block_hash[:self.difficulty]
        first_chars = first_chars.replace('0', '')  # remove os zeros
        if first_chars:
            return False  # first_chars não está vazia
        return True

    def verify_transactions(self, block):
        current_state = self.get_current_state()
        candidate_state = current_state.copy()

        print(block.transactions)

        # valida a primeira transação
        if len(block.transactions[0].keys()) > 1 or sum(block.transactions[0].values()) > 10:
            return False

        # itera sobre as transações restantes
        for transaction in block.transactions[1:]:
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

        return True


def verify_size(block):
    return 2 <= len(block.transactions) <= 10


def rebuild_block(data):
    block = Block(data['index'], data['prev_hash'])
    block.nonce = data['nonce']
    block.transactions = data['transactions']
    return block


# test
# from Miner import Miner
#
#
# a = Node('123')
# a.miner = Miner(a,'111',1)
# a.miner.start()
# a.miner.accept_transaction({'1': -2, '100': 2})
# a.miner.accept_transaction({'1': -2, '100': 2})
