from logic.Snake import Snake

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


class DangerousSnake(Snake):
    __ld50_mg = 0.0
    __venom_type = ""
    __avgvenom_yield = 0.0

    # class definition/constructor
    def __init__(self, name, scientific_name, family, genus, species,
                 ld50_mg, venom_type, avgvenom_yield, save=False):
        self.__ld50_mg = ld50_mg
        self.__venom_type = venom_type
        self.__avgvenom_yield = avgvenom_yield
        super().__init__(name, scientific_name, family, genus, species, save=save)

    def to_dict(self):
        dict = super().to_dict()
        dict["type"] = "Dangerous Snake"
        dict["ld50_mg"] = self.__ld50_mg
        dict["venom_type"] = self.__venom_type
        dict["avgvenom_yield"] = self.__avgvenom_yield
        return dict

    def get_key(self):
        return (f"{self.get_name()}:{self.get_scientific_name()}, LD50 rating {self.__ld50_mg} with "
                f"venom/toxin type: {self.__venom_type}").lower()

    def get_printable_key(self):
        return (f"{self.get_name()}:{self.get_scientific_name()}, LD50 rating {self.__ld50_mg} with "
                f"venom/toxin type: {self.__venom_type}")

    @staticmethod
    def make_key(name, scientific_name, ld50_mg, venom_type):
        return (f"{name}:{scientific_name}, LD50 rating {ld50_mg} with "
                f"venom/toxin type: {venom_type}").lower()

    def __str__(self):
        string = super().__str__()
        return (f"{string} with LD50 mg rating {self.__ld50_mg} with toxin type: {self.__venom_type} and venom yield mg"
                f": {self.__avgvenom_yield}")

    def to_html(self):
        html = super().to_html()
        return html + (f" with LD50 mg rating: {self.__ld50_mg} with toxin type: {self.__venom_type} and venom yield"
                       f" in mg: {self.__avgvenom_yield}")
