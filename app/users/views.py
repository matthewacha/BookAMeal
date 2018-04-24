from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from . import users
from .model import database, User
import jwt
import datetime

userapi=Api(users)
SECRET_KEY = 'VX-4178-WD-3429-MZ-31'

class signup(Resource):
    def post(self):
        json_data = request.get_json()
        """Check that email format is correct"""
        if json_data['email'].lower().endswith('.com') is False:
            return make_response((jsonify({"message":"Input a valid email"})), 422)
        if '@' not in json_data['email'][:-4]:
            return make_response((jsonify({"message":"Input a valid email"})), 422)
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
                        'user_id':user.generate_id(len(database))}

        """Add user to database"""
        database.append(user_profile)
        return make_response((jsonify({"message":"Successfully signed up"})), 201)
    
class login(Resource):
    def post(self):
        auth = request.get_json()
        """Check auth is sent"""
        if not auth or not auth['email'] or not auth['password']:
            return make_response(("Authorize with email and password"), 401)

        """Check that email format is correct"""
        try:
            if auth['email'].lower().endswith('.com') is False:
                return make_response((jsonify({"message":"Input a valid email"})), 401)
            if '@' not in auth['email'][:-4]:
                return make_response((jsonify({"message":"Input a valid email"})), 401)
            repeat = [char for char in auth['email'] if char == '@']
            if len(repeat) >1:
                return make_response((jsonify({"message":'''Repetition of "@" is not allowed'''})), 422)
        except AttributeError as e:
            return make_response((jsonify({"message":"Input should be a string"})), 500)

        """Check if user in databse"""
        user = [user for user in database if user['details'].email.lower() == auth['email'].lower()]
        if len(user) == 0 :
            return make_response((jsonify({"message":"User does not exist"})), 404)

        """Check if password matches"""
        info = user[0]
        if check_password_hash(info['details'].password, auth['password']):
            """Generate token on login"""
            token = jwt.encode({
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 0, minutes = 45),
                "iat": datetime.datetime.utcnow(),
                "sub": info['user_id']}, SECRET_KEY, algorithm = 'HS256')
            return jsonify({'token':token})
        else:
            return make_response(("Authorize with correct password"), 401)
        


userapi.add_resource(signup, 'auth/signup')
userapi.add_resource(login, 'auth/login')
