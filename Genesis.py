class Genesis:
    def __init__(self):
        self.transactions = list()
        self.index = 0
        self.transactions.append({'1': 100, '2': 100})

    def __str__(self):
        return str(self.__dict__)
