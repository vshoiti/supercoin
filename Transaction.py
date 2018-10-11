class Transaction:

    def __init__(self, sender, receiver, amount, time_stamp):
        self.sender = -amount
        self.receiver = amount

    def __str__(self):
        return str('0')
