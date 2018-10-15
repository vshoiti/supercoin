class Genesis:
    def __init__(self):
        self.transactions = list()
        self.nonce = 0
        self.index = 0
        self.transactions.append({'1': 100, '2': 100})
        self.prev_hash = ''

    def __str__(self):
        # montagem manual da string pois self.__dict__ não ordenava deterministicamente os items
        self_string = "{"
        self_string += "'nonce': " + str(self.nonce) + ", "
        self_string += "'index': " + str(self.index) + ", "
        self_string += "'prev_hash': '" + str(self.prev_hash) + "', "
        self_string += "'transactions': " + str(self.transactions) + "}"
        return self_string
