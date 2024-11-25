from logic.Snake import Snake
from logic.DangerousSnake import DangerousSnake
from ui.input_validation import select_item, input_string, y_or_n, get_real
from logic.HabitatList import HabitatList


# ***************************************************************
# Author: (Dusan Dusko Ulemek)
# Lab: (Lab 9)
# Date: (11/23/2024)
# Description: OOP program that has class Snake, subclass
# dangerous snake, and a category class of Habitat (Snake)
# Input: user will have various selections to make to see
# print items, show items, add item to category, remove item
# from category, create/delete category as well as item,
# show category and contents, etc
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

class ConsoleUI:
    __all_snakes = None
    __all_habitat_lists = []

    # Constant/ List of choices
    CHOICES = ["list", "habitat", "create", "delete", "show", "include", "discard", "add", "exclude", "update", "join",
               "exit"]

    @classmethod
    # Method to initialize class
    def init(cls):
        cls.__all_snakes, cls.__all_habitat_lists = HabitatList.read_data()

    @classmethod
    def select_habitatlist(cls, include_all_snakes=False):
        names = []
        map = {}
        position = 1
        for habitatlist in cls.__all_habitat_lists:
            if include_all_snakes or habitatlist.get_habitat_name != HabitatList.ALL_SNAKES:
                names.append(habitatlist.get_habitat_name())
                map[str(position)] = habitatlist.get_habitat_name()
                position += 1
        names.append("None")
        map[str(position)] = "None"
        print("Please select a snake habitat list from the choices given below! ")
        position = 1
        for name in names:
            print(f"   {position}: {name}")
            position += 1
        name = select_item("Select a habitat list or type in 'None' to exit: ", items=names, mapping=map)
        if name == "None":
            return None
        habitatlist = HabitatList.lookup(name)
        return habitatlist

    @classmethod
    def select_snake(cls, habitatlist=None):
        if habitatlist is None:
            habitatlist = cls.__all_snakes
        keys = []
        map = {}
        position = 1
        for snake in habitatlist:
            keys.append(snake.get_key())
            map[str(position)] = snake.get_key()
            position += 1  # increment
        keys.append("None")
        map[str(position)] = "None"
        print("Please select a snake from the list below! ")
        position = 1
        for key in keys:
            print(f"    {position}: {key}")
            position += 1
        key = select_item("Enter snake or type in 'None' to exit: ", items=keys, mapping=map)
        if key == "None":
            return None
        snake = Snake.lookup(key)
        return snake

    @classmethod
    def list_snakes(cls):
        for snake in cls.__all_snakes:
            print(snake.get_key(), ":", snake, sep="")

    @classmethod
    def list_habitats(cls):
        for habitat in cls.__all_habitat_lists:
            print(f"{habitat.get_habitat_name()}:{habitat.get_geographic_location()}")

    @classmethod
    def create_habitat(cls):
        # habitat_name, geographic_description, habitat_list
        habitat_name = input_string("Please enter the name of new habitat or 'None' to exit: ",
                                    "Name must be non empty!!: ")
        if habitat_name == "None":
            return None
        geographic_description = input_string("Please enter the description of habitat: "
                                              , valid=lambda x: True)
        habitatlist = HabitatList.lookup(habitat_name)
        if habitatlist is not None:
            print("Error, habitat exists already!!")
            return
        habitatlist = HabitatList(habitat_name, geographic_description, [], save=True)
        cls.__all_habitat_lists.append(habitatlist)
        print("SUCCESS! Habitat has now been created!")

    @classmethod
    def delete_habitat(cls):
        habitatlist = cls.select_habitatlist()
        if habitatlist is None:
            # print(f"No such habitat exists")
            return
        cls.__all_habitat_lists.remove(habitatlist)  # removes habitat from list of all habitats
        habitatlist.delete()
        print("Habitat deleted!")

    @classmethod
    def show_habitatlist(cls):
        habitatlist = cls.select_habitatlist(True)
        if habitatlist is None:
            return
        print(f"Habitat Name: {habitatlist.get_habitat_name()}")
        print(f"Geographic Description: {habitatlist.get_geographic_location()}")
        print("Snakes in the given habitat: ")
        for habitat in habitatlist:
            print("   ", habitat)

    @classmethod
    def include_snake(cls):
        is_dangerous_snake = y_or_n("is the new snake being added a dangerous snake (y/n)?: ")
        # name, scientific_name, family, genus, species
        name = input_string("What is the name of the snake?: ")
        scientific_name = input_string("What is the scientific name of the snake?: ")
        if is_dangerous_snake == "n" or is_dangerous_snake == "no":
            key = Snake.make_key(name, scientific_name)
            snake = Snake.lookup(key)
            if snake is not None:
                print("This Snake already exists! Try again please!")
                return
        if is_dangerous_snake == "y" or is_dangerous_snake == "yes":
            ld50_mg = get_real("Enter the LD50 in mg Sub: ", le=12.0, ge=0.0)
            venom_type = input_string("Enter venom type (ex: neurotoxic/cardiotoxic): ")
            avgvenom_yield = get_real("Enter the avg venom yield in mg: ", le=1000, ge=0.0)
            key = DangerousSnake.make_key(name, scientific_name, ld50_mg, venom_type)
            snake = DangerousSnake.lookup(key)
            if snake is not None:
                print("This dangerous Snake already exists in our database!")
                return
        family = input_string("What is the family of the snake?: ")
        genus = input_string("What is the genus of the snake?: ")
        species = input_string("What is the species of the snake?: ")
        if is_dangerous_snake == "y" or is_dangerous_snake == "yes":
            snake = DangerousSnake(name, scientific_name, family, genus, species, ld50_mg, venom_type, avgvenom_yield,
                                   save=True)
        else:
            snake = Snake(name, scientific_name, family, genus, species, save=True)
        cls.__all_snakes.append(snake)
        print("SUCCESS! Snake has been made!")

    @classmethod
    def discard_snake(cls):
        snake = cls.select_snake()
        if snake is None:
            return
        for habitatlist in cls.__all_habitat_lists:
            if snake in habitatlist:
                habitatlist.remove(snake)
        snake.delete()
        print("SUCCESS! Snake has been deleted")

    @classmethod
    def add_snake(cls):
        habitatlist = cls.select_habitatlist()
        if habitatlist is None:
            return
        snake = cls.select_snake()
        if snake is None:
            return
        if snake in habitatlist:
            print("Snake already in the habitat list!")
            return
        habitatlist.append(snake)
        print("Snake added to the habitat!")

    @classmethod
    def exclude_snake(cls):
        habitatlist = cls.select_habitatlist()
        if habitatlist is None:
            return
        snake = cls.select_snake(habitatlist)
        if snake is None:
            return
        if snake not in habitatlist:
            print("Error! The snake is not in the habitat")
            return
        habitatlist.remove(snake)
        print("Snake removed from habitat!")

    @classmethod
    def update_snake(cls):
        snake = cls.select_snake()
        if snake is None:
            return
        family = input_string("Enter the new family of the snake: ", valid=lambda x: True)
        snake.update_snake(family)
        print("Snake family updated!")

    @classmethod
    def join_habitatlists(cls):
        habitatlist1 = cls.select_habitatlist(include_all_snakes=True)
        if habitatlist1 is None:
            return
        habitatlist2 = cls.select_habitatlist(include_all_snakes=True)
        if habitatlist2 is None:
            return
        new_habitalist = habitatlist1 + habitatlist2
        cls.__all_habitat_lists.append(new_habitalist)
        print("Habitats have been jointed together!")

    @staticmethod
    def print_menu():
        print("Please choose option from the list below:")
        print("  list - Print all snakes")
        print("  habitat - Print all snake habitats")
        print("  create - create a new habitat")
        print("  delete - delete a habitat")
        print("  show - show all snake habitats")
        print("  include - Create a Snake")
        print("  discard - delete a snake")
        print("  add - add snake to a habitat")
        print("  exclude - remove a snake from habitat")
        print("  update - update a family for a snake")
        print("  join   - join two habitats together")
        print("  exit - Exit the Menu")

    # Run Method
    @classmethod
    def run(cls):
        while True:
            cls.print_menu()
            choice = select_item("Please select an option: ", "Selection must be in the menu!",
                                 cls.CHOICES)
            if choice == "exit":
                break
            elif choice == "list":
                cls.list_snakes()
            elif choice == "habitat":
                cls.list_habitats()
            elif choice == "create":
                cls.create_habitat()
            elif choice == "delete":
                cls.delete_habitat()
            elif choice == "show":
                cls.show_habitatlist()
            elif choice == "include":
                cls.include_snake()
            elif choice == "discard":
                cls.discard_snake()
            elif choice == "add":
                cls.add_snake()
            elif choice == "exclude":
                cls.exclude_snake()
            elif choice == "update":
                cls.update_snake()
            elif choice == "join":
                cls.join_habitatlists()
            print()
        print("Thanks for your using our program!")
        print("Goodbye for now!")


if __name__ == "__main__":
    ConsoleUI.init()
    ConsoleUI.run()
