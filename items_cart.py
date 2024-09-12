from abc import ABC, abstractmethod

class cartItem(ABC):

    def __init__(self, itemName, itemID, price, quantity, itemType = 'Item') :
        self.__itemName = itemName
        self.__itemID = itemID
        self.__price = price
        self.__quantity = quantity
        self.__itemType = itemType

    @property
    def _itemName(self):
        return self.__itemName
    '''
    @_itemName.setter
    def _itemName(self, value):
        self.__itemName = value
    '''
    @property
    def _itemID(self):
        return self.__itemID
    '''
    @_itemID.setter
    def _itemID(self, value):
        self.__itemID = value
    '''
    @property
    def _price(self):
        return self.__price
    '''
    @_price.setter
    def _price(self, value):
        self.__price = value
    '''
    @property
    def _quantity(self):
        return self.__quantity
    
    @_quantity.setter
    def _quantity(self, value):
        self.__quantity = value
    
    @property
    def _itemType(self):
        return self.__itemType
    '''
    @_itemType.setter
    def _itemType(self, value):
        self.__itemType = value
    '''