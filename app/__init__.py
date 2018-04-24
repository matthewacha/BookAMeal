from flask import Flask
from flask_script import Manager
import config

APP = Flask(__name__)

APP.config.from_object("config")

from app.v1.users import usersv1 as users_v1
APP.register_blueprint(users_v1)
