from abc import ABC, abstractmethod

class cartItem(ABC):

    def __init__(self, itemName, itemID, price, quantity=1):
        self.__itemName = itemName
        self.__itemID = itemID
        self.__price = price
        self.__quantity = quantity