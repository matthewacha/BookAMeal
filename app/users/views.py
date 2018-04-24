from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from . import users
from .model import database, User

userapi=Api(users)

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
            return make_response((jsonify({"message":"User already exists"})), 501)

        """Create object user"""
        user = User(json_data['email'], generate_password_hash(json_data['password']))
        user_profile = {'details':user,
                        'user_id':user.generate_id(len(database))}

        """Add user to database"""
        database.append(user_profile)
        return jsonify({"message":"Successfully signed up"})
    
class login(Resource):
    def post():
        pass
        


userapi.add_resource(signup, 'auth/signup')
userapi.add_resource(login, 'auth/login')
