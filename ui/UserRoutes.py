from ui.WebUI import WebUI
from flask import render_template, request, session, redirect, url_for
from logic.HabitatList import HabitatList
from logic.Snake import Snake
from logic.DangerousSnake import DangerousSnake
from logic.User import User

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


class UserRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/get_user")  # will get the currently logged in user
    def get_user():
        if "username" in session:
            return session["username"]
        else:
            return "None"

    @staticmethod
    @__app.route("/set_user")
    def set_user():
        if "username" in request.args:
            session["username"] = request.args["username"]
            return "User set."
        if "username" in session:
            del session["username"]  # removes the value from flask object session
        return "User cleared"

    @staticmethod
    @__app.route("/login")
    def login():
        return render_template("user/login.html")

    @staticmethod
    @__app.route("/do_login", methods=['GET', 'POST'])
    def do_login():
        username, error = WebUI.validate_field("Username", "username")
        if error is not None:
            return error
        password, error = WebUI.validate_field("Password", "password")
        if error is not None:
            return error
        user = User.read_user(username)
        if user is None:
            return render_template("error.html",
                                   message_header="Login failed!",
                                   message_body="The log in attempt failed. Please check your account"
                                                " information and try again!")
        logged_in = user.verify_password(password)
        if not logged_in:
            return render_template("error.html",
                                   message_header="Login failed!",
                                   message_body="The log in attempt failed. Please check your account information "
                                                " and try again!")
        session["user"] = user  # store on session
        return redirect(url_for("homepage"))

    @staticmethod
    @__app.route("/logout")
    def logout():
        if "user" in session:
            del session["user"]
        return redirect(url_for("login"))
