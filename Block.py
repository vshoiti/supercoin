class Block:
    def __init__(self, index, prev_hash):
        self.nonce = 0
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = []

    def __str__(self):
        self_dict = {}  # montagem manual do dict pois self.__dict__ não ordenava deterministicamente os itens
        self_dict['nonce'] = self.nonce
        self_dict['index'] = self.index
        self_dict['prev_hash'] = self.prev_hash
        self_dict['transactions'] = self.transactions
        return str(self_dict)
