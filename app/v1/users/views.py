from flask import Flask, jsonify, request, make_response
import flask_restful
from flask_restful import Resource, Api
from flasgger.utils import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from . import users
from app.models import database, User
import jwt
import datetime
from functools import wraps

userapi=Api(users)
SECRET_KEY = 'VX-4178-WD-3429-MZ-31'

def token_required(funct):
    @wraps(funct)
    def verify_token(*args, **kwargs):
        token = None
        if 'access_token' in request.headers:
            token = request.headers['access_token']
            try:
                data = jwt.decode(token, SECRET_KEY)
                current_user = {}
                for user in database:
                     if user['user_id'] == data["sub"]:
                         current_user["user_id"] = user["user_id"]
                         current_user["Admin_status"] = user["Admin_status"]
                         current_user["email"] = user["details"].email
            except:
                return make_response((jsonify({"message":"Unauthorized access, please login"})),401)
            return funct(current_user, *args, **kwargs)
        return make_response((jsonify({"message":"Token is missing"})),401) 
    return verify_token

class signup(Resource):
    @swag_from('signup.yml')
    def post(self):
        json_data = request.get_json()
        """Check that email format is correct"""
        if json_data['email'].lower().endswith('.com') is False:
            return make_response((jsonify({"message":"Input a valid email"})), 422)
        if '@' not in json_data['email'][:-4]:
            return make_response((jsonify({"message":'''"@" is missing'''})), 422)
        repeat = [char for char in json_data['email'] if char == '@']
        if len(repeat) >1:
            return make_response((jsonify({"message":'''Repetition of "@" is not allowed'''})), 422)

        """Check that user is unique"""
        user_ = [user for user in database if json_data['email'].lower() == user['details'].email.lower()]

        if len(user_) != 0:
            return make_response((jsonify({"message":"User already exists"})), 401)

        """Create object user"""
        user = User(json_data['email'], generate_password_hash(json_data['password']))
        user_profile = {'details':user,
                        'user_id':user.generate_id(len(database)),
                        'Admin_status':False}

        """Add user to database"""
        database.append(user_profile)
        return make_response((jsonify({"message":"Successfully signed up"})), 201)
    
class login(Resource):
    @swag_from('login.yml')
    def post(self):
        auth = request.get_json()
        if not auth or not auth['email'] or not auth['password']:
            return make_response((jsonify({"message":"Authorize with email and password"})), 401)
        if isinstance(auth['email'], int):
            return make_response((jsonify({"message":"Input should be a string"})), 401)
        if '@' not in auth['email'][:-4]:
            return make_response((jsonify({"message":'''"@" is missing'''})), 401)
        if auth['email'].lower().endswith('.com') is False:
            return make_response((jsonify({"message":"Input a valid email"})), 401)
        repeat = [char for char in auth['email'] if char == '@']
        if len(repeat) > 1:
            return make_response((jsonify({"message":'''Repetition of "@" is not allowed'''})), 401)
        """Verify user in database and password matches"""
        user = [user for user in database if user['details'].email.lower() == auth['email'].lower()]
        if len(user) == 0 :
            return make_response((jsonify({"message":"User does not exist"})), 404)
        info = user[0]
        if check_password_hash(info['details'].password, auth['password']):
            token = jwt.encode({
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 0, minutes = 45),
                "iat": datetime.datetime.utcnow(),
                "sub": info['user_id']}, SECRET_KEY, algorithm = 'HS256')
            return jsonify({'token':token})
        else:
            return make_response((jsonify({"message":"Authorize with correct password"})), 401)
        
class Admin(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/changeAdmin.yml')
    def put(self, current_user):
        count=0
        for user in database:
            if user['user_id'] == current_user['user_id']:
                user['Admin_status'] = request.get_json('Admin_status', user['Admin_status'])
                count += 1
        if count == 1:
            return make_response((jsonify({"message":"Admin status set to True"})), 201)
    
    method_decorators=[token_required]
    @swag_from('api-docs/checkAdmin.yml')
    def get(self,current_user):
        return make_response((jsonify({"Admin_status":current_user["Admin_status"]})), 200)

userapi.add_resource(signup, 'auth/signup')
userapi.add_resource(login, 'auth/login')
userapi.add_resource(Admin, 'auth/Admin')
