from ui.WebUI import WebUI
from flask import render_template, request
from logic.HabitatList import HabitatList
from logic.Snake import Snake
from logic.DangerousSnake import DangerousSnake

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


class UpdateRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/update_snake_family')
    def update_snake_family():
        return render_template("update/update_snake_family.html",
                               snakes=WebUI.get_all_snakes())

    @staticmethod
    @__app.route('/do_update_snake_family', methods=['GET', 'POST'])
    def do_update_snake_family():
        key, error = WebUI.validate_field("The snake", "snake")
        if key is None:
            return error
        snake = Snake.lookup(key)
        if snake is None:
            return render_template("error.html",
                                   message_header="Snake does not exist!",
                                   message_body=f"The snake {key} does not exist. Select another snake and Try again!")
        if "family" in request.form:
            family = request.form["family"].strip()
        else:
            family = ""
        snake.update_snake(family)
        return render_template("update/confirm_family_updated.html",
                               snake=snake)

    @staticmethod
    @__app.route('/add_snake_to_habitatlist')
    def add_snake_to_habitatlist():
        return render_template("update/add_snake_to_habitatlist.html",
                               snakes=WebUI.get_all_snakes(),
                               habitatlists=WebUI.get_all_habitatlists())

    @staticmethod
    @__app.route('/do_add_snake_to_habitatlist', methods=['GET', 'POST'])
    def do_add_snake_to_habitatlist():
        snake_key, error = WebUI.validate_field("The snake", "snake")
        if snake_key is None:
            return error
        snake = Snake.lookup(snake_key)
        if snake is None:
            return render_template("error.html",
                                   message_header="Snake does not exist!",
                                   message_body=f"The snake {snake_key} does not exist."
                                                f" Select another snake and Try again!")
        habitatlist_key, error = WebUI.validate_field("the habitatlist name"
                                                      , "habitatlist")
        if habitatlist_key is None:
            return error
        habitatlist = HabitatList.lookup(habitatlist_key.lower())
        if habitatlist is None:
            return render_template("error.html",
                                   message_header=f"The {habitatlist_key} was not found!",
                                   message_body=f"A Habitatlist with'{habitatlist_key}' was not found"
                                                f" Please try again!"
                                   )
        if snake in habitatlist:
            return render_template("error.html",
                                   message_header=f"The snake is in the habitatlist already!",
                                   message_body=f"The snake '{snake.get_printable_key()}' is already in the "
                                                f" '{habitatlist.get_printable_key()}' habitatlist!"
                                                f" Please try again!")
        habitatlist.append(snake)
        return render_template("update/confirm_snake_added_to_habitatlist.html", snake=snake,
                               habitatlist=habitatlist)

    @staticmethod
    @__app.route('/remove_snake_from_habitatlist')
    def remove_snake_from_habitatlist():
        return render_template("update/remove_snake_from_habitatlist.html",
                               snakes=WebUI.get_all_snakes(),
                               habitatlists=WebUI.get_all_habitatlists())

    @staticmethod
    @__app.route('/do_remove_snake_from_habitatlist', methods=['GET', 'POST'])
    def do_remove_snake_from_habitatlist():
        snake_key, error = WebUI.validate_field("The snake", "snake")
        if snake_key is None:
            return error
        snake = Snake.lookup(snake_key)
        if snake is None:
            return render_template("error.html",
                                   message_header="Snake does not exist!",
                                   message_body=f"The snake {snake_key} does not exist. "
                                                f" Select another snake and Try again!")
        habitatlist_key, error = WebUI.validate_field("the habitatlist name"
                                                      , "habitatlist")
        if habitatlist_key is None:
            return error
        habitatlist = HabitatList.lookup(habitatlist_key.lower())
        if habitatlist.get_habitat_name() == HabitatList.ALL_SNAKES:
            return render_template("error.html",
                                       message_header=f"Unable to remove snake!",
                                       message_body=f"Unable to remove snakes from the '{HabitatList.ALL_SNAKES}'"
                                                    f" habitatlist!")
        if habitatlist is None:
            return render_template("error.html",
                                   message_header=f"The {habitatlist_key} was not found!",
                                   message_body=f"A Habitatlist with name '{habitatlist_key}' was not found."
                                                f" Please try again!"
                                   )
        if snake not in habitatlist:
            return render_template("error.html",
                                   message_header=f"The snake is not in the habitatlist!",
                                   message_body=f"The snake '{snake.get_printable_key()}' is not in the "
                                                f" '{habitatlist.get_printable_key()}' habitatlist!"
                                                f" Please try again!")
        habitatlist.remove(snake)
        return render_template("update/confirm_snake_removed_from_habitatlist.html", snake=snake,
                               habitatlist=habitatlist)
