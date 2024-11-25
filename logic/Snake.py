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


class Snake:
    __name = " "
    __scientific_name = " "
    __family = " "
    __genus = " "
    __species = " "
    __map = {}

    def __init__(self, name, scientific_name, family, genus, species, save=False):
        self.__name = name
        self.__scientific_name = scientific_name
        self.__family = family
        self.__genus = genus
        self.__species = species
        self.__class__.__map[self.get_key()] = self
        if save:
            self.save()

    # wrapper for the constructor
    @classmethod
    def build(cls, snake_dict):
        from logic.DangerousSnake import DangerousSnake
        if snake_dict["type"] == "Snake":
            return Snake(snake_dict["name"],
                         snake_dict["scientific_name"],
                         snake_dict["family"],
                         snake_dict["genus"],
                         snake_dict["species"])
        elif snake_dict["type"] == "Dangerous Snake":
            return DangerousSnake(snake_dict["name"],
                                  snake_dict["scientific_name"],
                                  snake_dict["family"],
                                  snake_dict["genus"],
                                  snake_dict["species"],
                                  snake_dict["ld50_mg"],
                                  snake_dict["venom_type"],
                                  snake_dict["avgvenom_yield"])

    def to_dict(self):
        return {"_id": self.get_key(),
                "type": "Snake",
                "name": self.__name,
                "scientific_name": self.__scientific_name,
                "family": self.__family,
                "genus": self.__genus,
                "species": self.__species}

    def get_key(self):
        return f"{self.__name}:{self.__scientific_name}".lower()

    def get_printable_key(self):
        return f"{self.__name}:{self.__scientific_name}"

    @staticmethod
    def make_key(name, scientific_name):
        return f"{name}:{scientific_name}".lower()

    def get_name(self):
        return self.__name

    def get_scientific_name(self):
        return self.__scientific_name

    # Setter
    def update_snake(self, family):
        self.__family = family
        self.save()

    @classmethod
    def lookup(cls, key):
        if key in cls.__map:
            return cls.__map[key]
        else:
            return None

    def delete(self):
        from data.Database import Database
        del self.__class__.__map[self.get_key()]
        Database.delete_snake(self)

    def __str__(self):
        return f"{self.__name}:{self.__scientific_name}: {self.__family:} : {self.__genus}: {self.__species}"

    def to_html(self):
        return f"{self.__name}: {self.__scientific_name}: {self.__family:} : {self.__genus}: {self.__species}"

    @staticmethod
    def get_snakes():
        from data.Database import Database
        return Database.get_snake()

    def save(self):
        from data.Database import Database

        Database.save_snake(self)
