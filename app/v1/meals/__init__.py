from flask import Blueprint

meals = Blueprint('meals' , __name__, url_prefix='/api/v1/')

from . import views
