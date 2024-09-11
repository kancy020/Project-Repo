
#testing if payment work
class Order:

    allOrder = []

    def __init__(self, name, price, quantity=1) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity
        Order.allOrder.append(self)

    '''set the total price for item incase there amount of items being processed'''
    def get_total_price(self):
        return self.price * self.quantity
    
    def get_item_details(self):
        return{
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "totalPrice": self.get_total_price()
        }
    
class Payment:

    #could add in currency
    def __init__(self, balance) -> None:
        self.totalPrice = 0
        self.__balance = balance
        self.items = Order.allOrder.copy()
    

    '''adds the orders to items list to calculate total price'''
    def add_item(self, order):
        self.items.append(order)

    '''used to intiate the payment and prepare receipt'''
    def initiate_transaction(self):
        self.calculate_total_price()
        result = self.calculate_total_balance()
        if result:
            print(result)
        else:
            self.receipt()
            receipt = self.receipt()
            #this ensure the lists are cleared for each transaction
            self.items.clear()
            Order.allOrder.clear()

    '''calculates the total price for order'''
    def calculate_total_price(self):

        self.totalPrice = sum(item.get_total_price() for item in self.items)
        print("Processing Transaction\n")

    '''substracts the balance from total price'''
    def calculate_total_balance(self):
        if self.totalPrice > self.__balance:
            return "Transaction declined \nInsufficent balance"
        
        self.__balance -= self.totalPrice

        print("Finalising Transaction\n")

    '''output a recipt of total cost'''
    def receipt(self):
        receipt = {
            "totalPrice": self.totalPrice,
            "items": [item.get_details() for item in self.items]
        }

        return receipt



'''Testing order for payment'''    
# order1 = Order("Item1",10.00)
# order2 = Order("Item2",20.00,2)

# payment = Payment(1000.00)


# payment.initiate_transaction()

# order3 = Order("Item3",10.00)


# payment1 = Payment(1100.00)

# payment1.initiate_transaction()

# order4 = Order("Item3",10.00)


# payment2 = Payment(1.00)

# payment2.initiate_transaction()