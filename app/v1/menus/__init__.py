from flask import Blueprint

menus = Blueprint('menus' , __name__, url_prefix='/api/v1/')

from . import views
