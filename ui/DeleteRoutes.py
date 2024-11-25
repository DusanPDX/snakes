from ui.WebUI import WebUI
from flask import render_template, request
from logic.HabitatList import HabitatList
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

class DeleteRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/delete_habitatlist')
    def delete_habitatlist():
        return render_template("delete/delete_habitatlist.html",
                               habitatlists=WebUI.get_all_habitatlists())

    @staticmethod
    @__app.route('/do_delete_habitatlist', methods=['GET', 'POST'])
    def do_delete_habitatlist():
        habitatlist_key, error = WebUI.validate_field("the habitatlist name"
                                                      , "habitatlist")
        if habitatlist_key is None:  # if playlist key none, error returned
            return error
        habitatlist = HabitatList.lookup(habitatlist_key.lower())
        if habitatlist is None:
            return render_template("error.html",
                                   message_header=f"The habitatlist {habitatlist_key} was not found!",
                                   message_body=f"A habitatlist with name '{habitatlist_key}' was not found."
                                                f" Please try again!"
                                   )
        if habitatlist.get_habitat_name() == HabitatList.ALL_SNAKES:
            return render_template("error.html",
                                   message_header=f"Unable to delete habitatlist!",
                                   message_body=f"Unable to delete habitatlist '{HabitatList.ALL_SNAKES}'!"
                                   )
        WebUI.get_all_habitatlists().remove(habitatlist)  # removes habitat from list of all habitats
        habitatlist.delete()
        return render_template("delete/confirm_habitatlist_deleted.html",
                               habitatlist=habitatlist)

    @staticmethod
    @__app.route('/delete_snake')
    def delete_snake():
        return render_template("delete/delete_snake.html",
                               snakes=WebUI.get_all_snakes())

    @staticmethod
    @__app.route('/do_delete_snake', methods=['GET', 'POST'])
    def do_delete_snake():
        snake_key, error = WebUI.validate_field("The snake", "snake")
        if snake_key is None:
            return error
        snake = Snake.lookup(snake_key)
        if snake is None:
            return render_template("error.html",
                                   message_header="Snake does not exist!",
                                   message_body=f"The snake {snake_key} does not exist. "
                                                f"Select another snake and Try again!")
        for habitatlist in WebUI.get_all_habitatlists():
            if snake in habitatlist:
                habitatlist.remove(snake)
        snake.delete()
        return render_template("delete/confirm_snake_deleted.html", snake=snake)


