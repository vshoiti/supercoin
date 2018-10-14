import ast

from Genesis import Genesis
from Blockchain import Blockchain
from utils import hash_string


# TODO: mining and messaging


class Node:
    def __init__(self, address):
        self.address = address
        self.peers = []
        self.blockchain = Blockchain(Genesis())
        self.difficulty = 4
        self.current_state = None
        self.miner = None

    def get_current_state(self):
        if not self.current_state:
            return self.rebuild_current_state()
        return self.current_state

    # retorna um dict com todos os addresses existentes e seus fundos
    def rebuild_current_state(self):
        state = {}
        for transaction in self.blockchain.get_transactions():
            for address in transaction.keys():
                if address in state.keys():
                    state[address] += transaction[address]
                else:
                    state[address] = transaction[address]
        self.current_state = state
        return state

    def receive_block(self, new_block, sender_ip):
        last_block = self.blockchain.get_last()

        if new_block.index <= last_block.index:
            return False  # stale block

        else:
            # verifica o novo bloco e a chain a qual pertence, se diferente da atual
            self.validate_chain(new_block, sender_ip)

    def validate_chain(self, top_block, sender_ip):
        different_blocks = [top_block]
        top_index = top_block.index

        current_block = top_block
        # itera para encontrar blocos diferentes dos quais a blockchain atual armazena
        while self.blockchain.get_block(current_block.prev_hash) is None:
            current_block = self.request_block(current_block.prev_hash, sender_ip)  # pede o bloco diferente
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

    def validate_block(self, block):
        block_hash = hash_string(str(block))
        if not self.verify_size(block):
            return False
        if not self.verify_difficulty(block_hash):
            return False
        if not self.verify_transactions(block):
            return False

        print(block_hash, " accepted as valid")
        return True

    def request_block(self, block_hash, sender_ip):
        # TODO
        return sender_ip.blockchain.get_block(block_hash)

    def add_new_blocks(self, blocks, top_index):
        self.current_state = None  # inutiliza a referencia atual do estado
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

    def verify_size(self, block):
        return 2 <= len(block.transactions) <= 10

    def verify_transactions(self, block):
        current_state = self.get_current_state()
        candidate_state = current_state.copy()

        # valida a primeira transação
        if len(block.transactions[0].keys()) > 1 or block.transactions[0].values()[0] > 10:
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

    def start_miner(self):
        pass  # TODO

    def restart_miner(self):
        if self.miner:
            self.stop_miner()
            self.start_miner()

    def stop_miner(self):
        pass  # TODO

# node1 = Node(1)
# node2 = Node(2)
#
# genesis_hash = hash_string(str(Genesis()))
#
# a = Block(1, genesis_hash)
# # print(a)
#
# a.transactions.append({'1': -10, '2': 10})
#
# node2.blockchain.add_block(a, 1)
#
# node1.receive_block(a, node2)
#
# print(node2.blockchain.blocks)
# print(node1.blockchain.blocks)

# x = ast.literal_eval(str(a))
#
# print(x)
#
# x_txs = x['txs']
# for tx in x_txs:
#     print(x_txs[tx])

from Node import Node
from Miner import Miner


a = Node('123')
a.rebuild_current_state()
a.miner = Miner(a,'111',1)
a.miner.start()
a.miner.accept_transaction({'1':-2, '100':2})
a.miner.accept_transaction({'1':-2, '100':2})
