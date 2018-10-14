from utils import hash_string


class Blockchain:
    def __init__(self, genesis):
        self.blocks = list()
        self.blocks.append(genesis)

    def __str__(self):
        return str(self.__dict__)

    def get_last(self):
        return self.blocks[-1:][0]

    def get_size(self):
        return len(self.blocks)

    def get_block(self, block_hash):
        for block in self.blocks:
            if hash_string(str(block)) == block_hash:
                return block

        return None

    def add_block(self, block, index):
        assert index <= len(self.blocks)

        if index < len(self.blocks):
            self.blocks[index] = block
        else:
            self.blocks.append(block)

    def get_transactions(self):
        for block in self.blocks:
            for transaction in block.transactions:
                yield transaction
