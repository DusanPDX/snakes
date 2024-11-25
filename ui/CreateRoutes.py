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


class CreateRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/create_habitatlist')
    def create_habitatlist():
        return render_template("create/create_habitatlist.html")

    @staticmethod
    @__app.route('/do_create_habitatlist', methods=['GET', 'POST'])
    def do_create_habitatlist():
        habitat_name, error = WebUI.validate_field("The habitatlist name", "habitat_name")
        if habitat_name is None:
            return error
        key = habitat_name.lower()
        habitatlist = HabitatList.lookup(key)
        if habitatlist is not None:
            return render_template("error.html",
                                   message_header="Habitatlist already exists!!",
                                   message_body=f"A habitatlist named {habitat_name} already exists. Try again!")
        if "geographic_description" in request.form:
            geographic_description = request.form["geographic_description"].strip()
        else:
            geographic_description = ""
        habitatlist = HabitatList(habitat_name, geographic_description, [], save=True)
        WebUI.get_all_habitatlists().append(habitatlist)
        return render_template("create/confirm_habitatlist_created.html", habitatlist=habitatlist)

    @staticmethod
    @__app.route('/create_snake')
    def create_snake():
        return render_template("create/create_snake.html")

    @staticmethod
    @__app.route('/do_create_snake', methods=['GET', 'POST'])
    def do_create_snake():
        # name, scientific_name, family, genus, species
        name, error = WebUI.validate_field("The snake name", "name")
        if name is None:
            return error
        scientific_name, error = WebUI.validate_field("The snake scientific name", "scientific_name")
        if scientific_name is None:
            return error
        key = Snake.make_key(name, scientific_name).lower()
        snake = Snake.lookup(key)
        if snake is not None:
            return render_template("error.html",
                                   message_header=f"A snake already exists!!",
                                   message_body=f"A snake named {name} with scientific name {scientific_name}"
                                                f" already exists. Please try again!")
        family, error = WebUI.validate_field("The snake family", "family")
        if family is None:
            return error
        if "genus" in request.form:
            genus = request.form["genus"].strip()
        else:
            genus = ""
        if "species" in request.form:
            species = request.form["species"].strip()
        else:
            species = ""
        snake = Snake(name, scientific_name, family, genus, species, save=True)
        WebUI.get_all_snakes().append(snake)
        return render_template("create/confirm_snake_created.html", snake=snake)

    @staticmethod
    @__app.route('/create_dangerous_snake')
    def create_dangerous_snake():
        return render_template("create/create_dangerous_snake.html")

    @staticmethod
    @__app.route('/do_create_dangerous_snake', methods=['GET', 'POST'])
    def do_create_dangerous_snake():
        # name, scientific_name, family, genus, species
        name, error = WebUI.validate_field(" The dangerous snake name", "name")
        if name is None:
            return error
        scientific_name, error = WebUI.validate_field("The dangerous snake scientific name",
                                                      "scientific_name")
        if scientific_name is None:
            return error
        ld50_mg, error = WebUI.validate_field("The dangerous snake LD50mg", "ld50_mg")
        if ld50_mg is None:
            return error
        venom_type, error = WebUI.validate_field("The dangerous snake venom type", "venom_type")
        if venom_type is None:
            return error
        key = DangerousSnake.make_key(name, scientific_name, ld50_mg, venom_type).lower()
        snake = DangerousSnake.lookup(key)
        if snake is not None:
            return render_template("error.html",
                                   message_header=f"A dangerous snake already exists!!",
                                   message_body=f"A dangerous snake named {name} with scientific name {scientific_name}"
                                                f" that has ld50mg: {ld50_mg} already exists with"
                                                f" venom type {venom_type}. Please try again!")
        family, error = WebUI.validate_field("The dangerous snake family", "family")
        if family is None:
            return error
        if "genus" in request.form:
            genus = request.form["genus"].strip()
        else:
            genus = ""
        if "species" in request.form:
            species = request.form["species"].strip()
        else:
            species = ""
        if "avgvenom_yield" in request.form:
            avgvenom_yield = request.form["avgvenom_yield"].strip()
        else:
            avgvenom_yield = ""
        snake = DangerousSnake(name, scientific_name, family, genus, species,
                               ld50_mg, venom_type, avgvenom_yield, save=True)
        WebUI.get_all_snakes().append(snake)
        return render_template("create/confirm_dangerous_snake_created.html", snake=snake)

    @staticmethod
    @__app.route('/join_habitatlists')
    def join_habitatlists():
        return render_template("create/join_habitatlists.html",
                               habitatlists=WebUI.get_all_habitatlists())

    @staticmethod
    @__app.route('/do_join_habitatlists', methods=['GET', 'POST'])
    def do_join_habitatlists():
        first_key, error = WebUI.validate_field("the first habitatlist name"
                                                , "first_habitatlist")
        if first_key is None:
            return error
        second_key, error = WebUI.validate_field("the second habitatlist name"
                                                 , "second_habitatlist")
        if second_key is None:
            return error
        first_habitatlist = HabitatList.lookup(first_key.lower())
        if first_habitatlist is None:
            return render_template("error.html",
                                   message_header=f"The {first_key} was not found!",
                                   message_body=f"A Habitatlist with'{first_key}' was not found"
                                                f" Please try again!"
                                   )
        second_habitatlist= HabitatList.lookup(second_key.lower())
        if second_habitatlist is None:
            return render_template("error.html",
                               message_header=f"The {second_key} was not found!",
                               message_body=f"A Habitatlist with'{second_key}' was not found"
                                            f" Please try again!"
                               )
        new_key = f"{first_habitatlist.get_habitat_name()}/{second_habitatlist.get_habitat_name()}"
        new_habitatlist = HabitatList.lookup(new_key.lower())
        if new_habitatlist is not None:
            return render_template(
                "error.html",
                message_header=f"The habitatlist {new_key} already exists!!",
                message_body=f"A habitatlist with the name: {new_key} already exists."
                             f" Please choose another habitatlist and try once again! ")
        new_habitatlist = first_habitatlist + second_habitatlist
        WebUI.get_all_habitatlists().append(new_habitatlist)
        return render_template("create/confirm_habitatlists_joined.html",
                               first_habitatlist=first_habitatlist,
                               second_habitatlist=second_habitatlist,
                               new_habitatlist=new_habitatlist)






