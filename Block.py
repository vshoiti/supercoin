import ast

from Hasher import hash_string
from Node import Node
from Genesis import Genesis


class Block:
    def __init__(self, index, prev_hash):
        self.nonce = 0
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = []

    def __str__(self):
        return str(self.__dict__)


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