from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from logic.HabitatList import HabitatList
import os
import bcrypt

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


class WebUI:
    __all_snakes = None
    __all_habitat_lists = None
    __app = Flask(__name__)
    ALLOWED_PATHS = [
        "/login",
        "/do_login",
        "/static/dusko_snakes.css"

    ]        # everything we want user to see if they are not logged in!

    MENU = {
        "Print": {
            "print_habitatlist?habitatlist=all%20snakes": "Print a list of all the snakes",
            "print_habitatlists": "Print a list of all the snake habitats",
            "show_habitatlist_contents": "Select a habitatlist and show the contents"
        },
        "Create": {
            "create_snake": "Create a new snake",
            "create_dangerous_snake": "Create a new dangerous snake",
            "create_habitatlist": "Create a new snake habitat",
            "join_habitatlists": "Join two snake habitatlists together"

        },
        "Update": {
            "update_snake_family": "Update the family of snake",
            "add_snake_to_habitatlist": "Add a snake to a habitatlist",
            "remove_snake_from_habitatlist": "Remove a snake from a habitatlist",
        },
        "Delete": {
            "delete_snake": "Delete a snake",
            "delete_habitatlist": "Delete a habitatlist"
        }
    }

    @classmethod
    def get_app(cls):
        return cls.__app

    @classmethod
    def get_all_habitatlists(cls):
        return cls.__all_habitat_lists

    @classmethod
    def get_all_snakes(cls):
        return cls.__all_snakes

    @classmethod
    # Method to initialize class
    def init(cls):
        cls.__all_snakes, cls.__all_habitat_lists = HabitatList.read_data()

    @classmethod
    def validate_field(cls, obj_name, field_name):
        if field_name not in request.form:
            return None, render_template("error.html",
                                         message_header=f"{obj_name} not specified!",
                                         message_body=f"{obj_name} was not specified. "
                                                      f"Please check the form and try again!")
        field_val = request.form[field_name].strip()
        if field_val == "":
            return None, render_template("error.html",
                                         message_header=f"{obj_name} not specified!",
                                         message_body=f"{obj_name} was not specified. "
                                                      f"Please check the form and try again!")
        return field_val, None

    @staticmethod
    @__app.before_request
    def before_request():
        if "user" not in session:
            if request.path not in WebUI.ALLOWED_PATHS:
                return redirect(url_for("login"))



    @staticmethod
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    @__app.route('/')
    def homepage():
        return render_template("homepage.html", options=WebUI.MENU)

    @classmethod
    def run(cls):
        # need this
        from ui.PrintRoutes import PrintRoutes
        from ui.CreateRoutes import CreateRoutes
        from ui.UpdateRoutes import UpdateRoutes
        from ui.DeleteRoutes import DeleteRoutes
        from ui.UserRoutes import UserRoutes

        if "APPDATA" in os.environ:
            path = os.environ["APPDATA"]
        elif "HOME" in os.environ:
            path = os.environ["HOME"]
        else:
            raise Exception("Couldn't find config folder")  # raising exception

        cls.__app.secret_key = bcrypt.gensalt()  # will be a new random value every time web server restarted
        cls.__app.config["SESSION_TYPE"] = "filesystem"  # store in session files
        Session(cls.__app)  # connect the session mechanism that handles the requests to the flask app

        cls.__app.run(host="0.0.0.0", port=8443, ssl_context=(path + "/dusko_snakes/cert.pem",
                                                              path + "/dusko_snakes/key.pem"))
