from logic.Snake import Snake
from logic.DangerousSnake import DangerousSnake
from logic.HabitatList import HabitatList
from logic.User import User
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from configparser import ConfigParser
import os

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


class Database:
    __connection = None
    __database = None
    __snakes_collection = None
    __habitatlists_collection = None
    __users_collection = None
    APP_NAME = "dusko_snakes"

    # connect method
    @classmethod
    def connect(cls):
        if cls.__connection is None:
            if "APPDATA" in os.environ:
                path = f"{os.environ['APPDATA']}\\{cls.APP_NAME}\\{cls.APP_NAME}.ini"
            elif "HOME" in os.environ:
                path = f"{os.environ['HOME']}/{cls.APP_NAME}/{cls.APP_NAME}.ini"
            else:
                raise Exception("Couldn't find config directory!")

            config_parser = ConfigParser()
            config_parser.read(path)
            username = config_parser["Database"]["username"]
            password = config_parser["Database"]["password"]
            cluster = config_parser["Database"]["cluster"]

            uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0"
            cls.__connection = MongoClient(uri, server_api=ServerApi('1'))
            cls.__database = cls.__connection.DuskoSnakes
            cls.__snakes_collection = cls.__database.Snakes  # collection Snakes
            cls.__habitatlists_collection = cls.__database.HabitatLists  # collection
            cls.__users_collection = cls.__database.Users  # collection

            # print("Client:", cls.__connection)
            # print("Database:", cls.__database)
            # print("Snakes:", cls.__snakes_collection)
            # print("Habitatlists:", cls.__habitatlists_collection)

    @classmethod
    def rebuild_data(cls):
        cls.connect()
        # will drop/get rid of both collections
        cls.__snakes_collection.drop()  # drop snakes collection
        cls.__snakes_collection = cls.__database.Snakes
        cls.__habitatlists_collection.drop()  # drop habitat collection
        cls.__habitatlists_collection = cls.__database.HabitatLists
        cls.__users_collection.drop()  # drop users collection
        cls.__users_collection = cls.__database.Users  # makes a new collection

        # user objects
        user1 = User("Dusko", b'$2b$13$qvEu.PvXjRxIBD87ly93hezX.UXMthhFUvMpMhxw/ok3jMXG21m4G')
        user2 = User("Marc", b'$2b$13$nJWdalQC4isVBwBpd/jtn.OQgBeof7T5GhhgPoGe6tjDseusGz8Ou')

        user_dicts = [user.to_dict() for user in [user1, user2]]
        cls.__users_collection.insert_many(user_dicts)
        all_snakes, all_habitat_lists = cls.get_habitats()

        snake_dict = [snake.to_dict() for snake in all_snakes]
        cls.__snakes_collection.insert_many(snake_dict)

        habitatlist_dicts = [habitatlist.to_dict() for habitatlist in all_habitat_lists]
        cls.__habitatlists_collection.insert_many(habitatlist_dicts)

    @classmethod
    def read_data(cls):
        # reads the data from the MongoDB Database
        cls.connect()
        snake_dicts = list(cls.__snakes_collection.find())  # Read the snakes/ fetch out of the snakes collection
        snakes = [Snake.build(snake_dict) for snake_dict in snake_dicts]  # gives a list of the snakes
        habitat_dicts = list(cls.__habitatlists_collection.find())
        habitatlists = [HabitatList.build(habitat_dict) for habitat_dict in habitat_dicts]

        return HabitatList.lookup(HabitatList.ALL_SNAKES), habitatlists

    @classmethod
    def read_user(cls, username):
        user_dict = cls.__users_collection.find_one({"_id": username.lower()})
        if user_dict is None:
            return None
        else:
            return User.build(user_dict)

    @classmethod
    def get_habitats(cls):
        gs_tsi = Snake("Common garter snake", "Thamnophis sirtalis", "Colubridae",
                       "Thamnophis", "T. sirtalis")
        rn_dp = Snake("Ring-necked snake", "Diadophis punctatus", "Colubridae",
                      "Diadophis", "D. punctatus")
        ks_lc = Snake("California King Snake", "Lampropeltis californiae", "Colubridae",
                      "Lampropeltis", "L. californiae")
        gs_pc = Snake("Pacific gopher snake", "Pituophis catenifer", "Colubridae",
                      "Pituophis", "P. catenifer")
        bc_cc = Snake("Northern black racer", "Coluber constrictor constrictor", "Colubridae",
                      "Coluber", "C. constrictor")
        st_ct = Snake("sharp-tailed snake", "Contia tenuis", "Colubridae", "Contia",
                      "C.tenuis")
        ls_zs = Snake("Leopard snake", "Zamenis situla", "Colubridae", "Zamenis",
                      "Z. situla")
        cs_ti = DangerousSnake("Coastal taipan", "Oxyuranus scutellatus", "Elapidae",
                               "Oxyuranus", "O. scutellatus", 0.12, "Neurotoxic "
                               , 120)
        bm_dp = DangerousSnake("Black Mamba", "Dendroaspis polylepis", "Elapidae",
                               "Elapidae", "D. polylepis", 0.33,
                               "neurotoxic/cardiotoxic", 120)
        bs_pt = DangerousSnake("Eastern brown snake", "Pseudonaja textilis", "Elapidae",
                               "Pseudonaja", "P. textilis", 0.053, "Neurotoxic",
                               5)
        cc_no = DangerousSnake("Caspian Cobra", "Naja oxiana", "Elapidae", "Naja",
                               "N. oxiana", 0.21, "Neurotoxic", 75)
        it_om = DangerousSnake("Inland Taipan", "Oxyuranus microlepidotus", "Elapidae",
                               "Oxyuranus", "O. microlepidotus", 0.025,
                               "Neurotoxin,Myotoxin", 44)
        ys_hp = DangerousSnake("Yellow-bellied sea snake", "Hydrophis platurus", "Elapidae",
                               "Hydrophis", "H. platurus", 0.067, "Neurotoxic",
                               4.0)
        hn_hs = DangerousSnake("Hook-nosed sea snake", "Hydrophis schistosus", "Elapidae",
                               "Hydrophis", "H. schistosus", 0.1125,
                               "neurotoxin/myotoxin",
                               7.9)

        sea_sn = HabitatList("Sea", "Snakes that inhabit oceans/seas - mostly"
                                    " the Western Pacific", [ys_hp, hn_hs])
        for_sn = HabitatList("Forest", "Snakes that inhabit the woodlands, marshes,"
                                       " wooded areas,"
                                       "dense and light forests",
                             [st_ct, rn_dp, bc_cc, gs_pc, bm_dp])
        ar_sn = HabitatList("Desert", "Snakes that inhabit arid/dry "
                                      "and desert like landscapes,"
                                      "stony, rocky", [bs_pt, it_om, cc_no, gs_tsi, ls_zs])
        tr_sn = HabitatList("Tropical Rainforest",
                            " snakes that inhabit rainforests, jungles, tropical forests",
                            [cs_ti])
        all = HabitatList(HabitatList.ALL_SNAKES, "All snakes of all different "
                                                  "habitats", [gs_tsi, rn_dp, ks_lc, gs_pc, bc_cc, st_ct,
                                                               ls_zs, cs_ti, bm_dp, bs_pt, cc_no, it_om, ys_hp, hn_hs])

        return all, [sea_sn, for_sn, ar_sn, tr_sn, all]

    @classmethod
    def save_habitatlist(cls, habitatlist):
        cls.connect()
        cls.__habitatlists_collection.update_one({"_id": habitatlist.get_key()}, {"$set": habitatlist.to_dict()},
                                                 upsert=True)

    @classmethod
    def save_snake(cls, snake):
        cls.connect()
        cls.__snakes_collection.update_one({"_id": snake.get_key()}, {"$set": snake.to_dict()},
                                           upsert=True)

    @classmethod
    def delete_habitatlist(cls, habitatlist):
        cls.connect()
        cls.__habitatlists_collection.delete_one({"_id": habitatlist.get_key()})

    @classmethod
    def delete_snake(cls, snake):
        cls.connect()
        cls.__snakes_collection.delete_one({"_id": snake.get_key()})


if __name__ == "__main__":
    Database.connect()
    print(Database.read_user("Dusko"))
