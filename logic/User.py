import bcrypt


# ***************************************************************
# Author: (Dusan Dusko Ulemek)
# Lab: (Lab 9)
# Date: (11/23/2024)
# Description: OOP program that has class Snake, subclass
# dangerous snake, and a category class of Habitat (Snake)
# Input: user will have various selections to make to
# print items, show category and items, add item to category, remove item
# from category, create/delete category as well as item, etc
#
# Output: various - from new category added, to category
# deleted, deleting item (snake), creating snake (dangerous/non-dangerous)
# creating new snake habitatlist or deleting it, removing snake from habitat
# adding snake to a habitatlist, joining two habitatlists together, showing
# a habitat and the snakes that inhabit the chosen habitat, etc
#
# Sources: Lab Instructions, Marc's videos, Murcah python book
#
# Sample Run
# Sample Run not shown due to length/space of the content matter
#
# ***************************************************************


class User:
    __username = ""
    __hash = ""

    def __init__(self, username, hash):
        self.__username = username
        self.__hash = hash

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "username": self.__username,
            "hash": self.__hash
        }

    @classmethod
    def build(cls, dict):
        return cls(dict["username"], dict["hash"])     # will take dictionary from mongodb and return

    def get_key(self):
        return self.__username.lower()

    def get_username(self):
        return self.__username

    def get_hash(self):
        return self.__hash

    @staticmethod
    def read_user(username):
        from data.Database import Database
        return Database.read_user(username)

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.__hash)
