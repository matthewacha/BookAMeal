from flask import Flask
from flask_script import Manager
from config import config

APP = Flask(__name__)
set_environment=config.create_app('Development')
APP.config.from_object('set_environment')

from app.v1.users import usersv1 as users_v1
APP.register_blueprint(users_v1)