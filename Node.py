from Genesis import Genesis
from Blockchain import Blockchain
from Hasher import hash_string


class Node:
    def __init__(self, address):
        self.address = address
        self.blockchain = Blockchain(Genesis())
        self.difficulty = 0

    def receive_block(self, new_block, sender_ip):
        last_block = self.blockchain.get_last()

        if new_block.index <= last_block.index:
            return False  # stale block

        else:
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

        # adiciona os novos blocos até o maior índice válido
        self.add_blocks(different_blocks, top_index)

    def validate_block(self, block):
        block_hash = hash_string(str(block))
        if not self.verify_difficulty(block_hash):
            return False
        if not self.verify_transactions(block):
            return False

        return True

    def request_block(self, block_hash, sender_ip):
        # TODO
        return sender_ip.blockchain.get_block(block_hash)

    def add_blocks(self, blocks, top_index):
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
        return True  # TODO
