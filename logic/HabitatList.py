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


class HabitatList:
    ALL_SNAKES = "All Snakes"
    __habitat_name = ""  # habitat for snakes, sea desert, forest, etc
    __geographic_description = ""
    __habitat_list = []  # list of snakes in habitat
    __map = {}  # class property that maps from key value back to the playlist that matches the key

    def __init__(self, habitat_name, geographic_description, habitat_list, save=False):
        self.__habitat_name = habitat_name  # name in lower case is the key for one type of habitat
        self.__geographic_description = geographic_description
        self.__habitat_list = habitat_list
        self.__class__.__map[self.get_key()] = self  # going to return the key
        if save:
            self.save()

    @classmethod
    def build(cls, habitat_dict):
        from logic.Snake import Snake
        return HabitatList(
            habitat_dict["habitat_name"],
            habitat_dict["geographic_description"],
            [Snake.lookup(key) for key in habitat_dict["habitat_list"]]
        )

    def to_dict(self):
        return {"_id": self.get_key(),
                "habitat_name": self.__habitat_name,
                "geographic_description": self.__geographic_description,
                "habitat_list": [snake.get_key() for snake in self.__habitat_list]
                }

    def get_key(self):
        return self.__habitat_name.lower()

    def get_printable_key(self):
        return self.__habitat_name

    def get_habitat_name(self):
        return self.__habitat_name

    def get_geographic_location(self):
        return self.__geographic_description

    def __str__(self):
        s = f"""Habitat Name:{self.__habitat_name}
Geographic Description:{self.__geographic_description}
Habitat Snakes: 
"""
        for habitat_list in self.__habitat_list:
            s += "   " + str(habitat_list) + "\n"
        return s

    @classmethod
    def lookup(cls, key):
        lower_key = key.lower()
        if lower_key in cls.__map:
            return cls.__map[lower_key]
        else:
            return None

    # appends a snake in list of snakes in habitat
    def append(self, snake, save=True):
        from data.Database import Database
        self.__habitat_list.append(snake)
        if save:
            Database.save_habitatlist(self)

    # removes a snake in list of snakes in habitat
    def remove(self, snake):
        from data.Database import Database
        self.__habitat_list.remove(snake)
        Database.save_habitatlist(self)

    def delete(self):
        from data.Database import Database
        del self.__class__.__map[self.get_key()]
        Database.delete_habitatlist(self)

    def __iter__(self):
        return self.__habitat_list.__iter__()

    def contains(self, snake):
        return snake in self.__habitat_list

    def __add__(self, other):
        habitat_name = f"{self.get_habitat_name()}/{other.get_habitat_name()}"
        geographic_description = self.__geographic_description + " " + other.__geographic_description
        new_habitatlist = HabitatList(habitat_name, geographic_description, [])
        for snake in self:
            if snake not in new_habitatlist:
                new_habitatlist.append(snake, save=False)
        for snake in other:
            if snake not in new_habitatlist:
                new_habitatlist.append(snake, save=False)
        new_habitatlist.save()
        return new_habitatlist

    @staticmethod
    def get_habitats():
        from data.Database import Database

        return Database.get_habitats()

    @staticmethod
    def save(self):
        from data.Database import Database

        Database.save_snake(self)

    @staticmethod
    def rebuild_data():
        from data.Database import Database

        return Database.rebuild_data()

    @staticmethod
    def read_data():
        from data.Database import Database

        return Database.read_data()

    def save(self):
        from data.Database import Database

        Database.save_habitatlist(self)

