from abc import ABC, abstractmethod

class cartItem(ABC):

    def __init__(self, itemName, itemID, price, quantity, itemType = 'Item') :
        self.__itemName = itemName
        self.__itemID = itemID
        self.__price = price
        self.__quantity = quantity
        self.__itemType = itemType