from flask import Flask
from flask_script import Manager

APP = Flask(__name__)

APP.config.from_object("config")

from app.users import users as users
APP.register_blueprint(users)

from app.meals import meals as meals
APP.register_blueprint(meals)
