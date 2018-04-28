"""Initialize the app"""
from flask import Flask
from flasgger import Swagger
from flask_script import Manager
from app.v1.users import users as users
from app.v1.meals import meals as meals
from app.v1.menus import menus as menus
from app.v1.orders import orders as orders

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



APP.register_blueprint(users)


APP.register_blueprint(meals)


APP.register_blueprint(menus)


APP.register_blueprint(orders)
