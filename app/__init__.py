from flask import Flask
from flask_script import Manager
import config

APP = Flask(__name__)

APP.config.from_object("config")

from app.users import users as users_v1
APP.register_blueprint(users_v1)
