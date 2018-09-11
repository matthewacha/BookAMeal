"""Initialize the app"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS


def create_app(dev_state):
    if dev_state == 'Development':
        APP = Flask(__name__)
        APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', "postgresql://matthewacha:password@localhost/BookAMeal")
        print('working....')
        APP.config.from_object("config")
        APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        APP.config['SQLALCHEMY_BINDS'] = None
        APP.config['SECRET_KEY'] = 'VX-4178-WD-3429-MZ-31'
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

        return APP

   
APP = create_app('Development')
SWAGGER = Swagger(APP)
CORS(APP)
DB = SQLAlchemy(APP)
DB.init_app(APP) 


from . import views

