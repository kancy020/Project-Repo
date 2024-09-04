class Store:
    def __init__(self, id, name, address, date_created):
        self.id = id
        self.name = name
        self.address = address
        
class MenuItem:
    def __init__(self, name, price, store):
        self.name = name
        self.price = price
        self.store = store