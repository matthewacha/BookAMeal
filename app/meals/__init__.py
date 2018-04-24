from flask import Blueprint

meals = Blueprint('meals' , __name__, url_prefix='/')

from . import views
