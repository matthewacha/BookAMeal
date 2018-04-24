from flask import Blueprint

usersv1 = Blueprint('users' , __name__, url_prefix='/')

from . import views
