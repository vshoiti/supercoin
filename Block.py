class Block:
    def __init__(self, index, prev_hash):
        self.nonce = 0
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = []

    def __str__(self):
        # montagem manual da string pois self.__dict__ não ordenava deterministicamente os items
        self_string = "{"
        self_string += "'nonce': " + str(self.nonce) + ", "
        self_string += "'index': " + str(self.index) + ", "
        self_string += "'prev_hash': '" + str(self.prev_hash) + "', "
        self_string += "'transactions': " + str(self.transactions) + "}"
        return self_string

# a = Block(1, '0000')
# print(a)
#
# b = eval(str(a))
# print(b)
#
# b = Block(b['index'], b['prev_hash'])
# print(b)