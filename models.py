class Store:
    def __init__(self, name, address):
        self.name = name
        self.address = address

class MenuItem:
    def __init__(self, name, price, store):
        self.name = name
        self.price = price
        self.store = store