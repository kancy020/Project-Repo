from flask import Flask
import items_cart

class Cart:
    def __init__(self):
        self.cart_list = []

    def add(self, new_obj):
        for obj in self.cart_list:
            if obj._itemName == new_obj._itemName and obj._itemType == new_obj._itemType:
                obj._quantity = new_obj._quantity + obj._quantity
                return
        self.cart_list.append(new_obj)

    def remove(self, item_name):
        for obj in self.cart_list:
            if obj._itemName  == item_name:
                self.cart_list.remove(obj)
                return
            
    def update(self, item_name, new_quantity):
        for obj in self.cart_list:
            if obj._itemName == item_name:
                obj._quantity = new_quantity
                return