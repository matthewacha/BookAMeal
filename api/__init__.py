"""Initialize the app"""
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS


def create_app(dev_state):
    if dev_state == 'Development':
        APP = Flask(__name__)
        CORS(APP,resources={r"/api/*": {"origins": "*"}},
        methods='GET, POST, PUT, DELETE, OPTIONS',
        allow_headers=["Content-Type",
                       "K_access_token",
                       "access_token",
                       "Access-Control-Allow-Credentials"],
        supports_credentials = True)
        APP.config['CORS_HEADERS'] = 'Content-Type'
        APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', "postgresql://matthewacha:password@localhost/BookAMeal")
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

    @APP.before_request
    def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp

        @APP.after_request
        def add_cors(resp):
            """
            Ensure all responses have the CORS headers.
            This ensures any failures are also accessible by the client.
            """
            resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
            resp.headers['Access-Control-Allow-Credentials'] = 'true'
            resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE'
            resp.headers['Access-Control-Allow-Headers'] = request.headers.get(
                'Access-Control-Request-Headers', 'Authorization')
            return resp
        

        return APP


APP = create_app('Development')
SWAGGER = Swagger(APP)
DB = SQLAlchemy(APP)
DB.init_app(APP) 


from . import views

