from flask import Flask
from flask_script import Manager

APP = Flask(__name__)

APP.config.from_object("config")

from app.v1.users import users as users
APP.register_blueprint(users)

from app.v1.meals import meals as meals
APP.register_blueprint(meals)

from app.v1.menus import menus as menus
APP.register_blueprint(menus)

from app.v1.orders import orders as orders
APP.register_blueprint(orders)
