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
        self_string += "'transactions': ["
        for transaction in self.transactions:
            self_string += transaction_str(transaction) + ','
        self_string = self_string[:-1] + "]}"
        return self_string
        
def transaction_str(transaction):
    string = '{'
    for key, value in sorted(transaction.items(), key=lambda x: x[1]): 
        string += ("'{}' : {}".format(key, value)) + ','
    string = string[:-1] + '}'
    return string

#a = Block(1, '0000')
#a.transactions.append({'a':33, 'b':-33})
#print(a)

#
# b = eval(str(a))
# print(b)
#
# b = Block(b['index'], b['prev_hash'])
# print(b)
