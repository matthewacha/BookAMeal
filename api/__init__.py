"""Initialize the app"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

APP = Flask(__name__)

APP.config.from_object("config")
APP.config['SWAGGER'] = {'swagger': '2.0', 'title': 'BookAMeal-api', 'description': "is a \
            web based app that enables caterers to setup menus,view customer \
            orders and also check order history, revenues for specific days", \
            'basePath': '', 'version': '0.0.1', 'contact': {
                'Developer': 'Matthew Wacha',
                'email': 'matthewacha@gmail.com'
            }, 'license': {
            }, 'tags': [
                {
                    'name': 'User',
                    'description': 'The user of the api'
                },
                {
                    'name': 'Meal',
                    'description': 'Meal option a caterer adds,updates, deletes'
                },
                {
                    'name': 'Menu',
                    'description': 'Menu a meal option is added to '
                },
                {
                    'name': 'Order',
                    'description': 'Meal request made by clients'}]}

SWAGGER = Swagger(APP)

DB = SQLAlchemy(APP)
DB.init_app(APP)


from . import views

