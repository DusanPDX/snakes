from ui.WebUI import WebUI
from flask import render_template, request
from logic.HabitatList import HabitatList

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


class PrintRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/print_habitatlists')
    def print_habitatlists():
        return render_template("print/print_habitatlists.html",
                               habitalists=WebUI.get_all_habitatlists())

    @staticmethod
    @__app.route('/print_habitatlist')
    def print_habitatlist():
        if "habitatlist" not in request.args:
            return render_template("error.html",
                                   message_header="Habitatlist not specified!",
                                   message_body="No snake habitat was specified. Please check the URL and try again!")
        key = request.args["habitatlist"]
        habitatlist = HabitatList.lookup(key)
        if habitatlist is None:
            return render_template("error.html",
                                   message_header="Habitatlist was not found!",
                                   message_body=f"The following snake habitat '{key}' was not found!"
                                                f" Please check the URL and try again!")
        return render_template("print/print_habitatlist.html", habitatlist=habitatlist)



    @staticmethod
    @__app.route('/show_habitatlist_contents')
    def show_habitatlist_contents():
        return render_template('print/show_habitatlist_contents.html',
                        habitatlists=WebUI.get_all_habitatlists())
