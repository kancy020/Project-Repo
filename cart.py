from flask import Flask
import items_cart

class Cart:
    def __init__(self):
        self.cart_list = []

    def add(self, new_obj):
        for obj in self.cart_list:
            if obj._itemID == new_obj._itemID:
                obj._quantity = new_obj._quantity + obj._quantity
                return
        self.cart_list.append(new_obj)

    def remove(self, item_id):
        for obj in self.cart_list:
            if obj._itemID  == item_id:
                self.cart_list.remove(obj)
                return


