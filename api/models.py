import re
from flask import Flask, jsonify, request, make_response
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from api import DB
import datetime

class User(DB.Model):
    __tablename__ = 'user'
    id = DB.Column(DB.Integer, primary_key=True)
    email = DB.Column(DB.String(60), unique=True)
    password = DB.Column(DB.String(300))
    admin_status = DB.Column(DB.Boolean, default=False)
    orders = DB.relationship('Order', backref='user')
    def __init__(self,email,password,admin_status=False):
        self.email = email
        self.password = password
        self.admin_status = admin_status

    @staticmethod
    def verify_input():
        auth = request.get_json()
        response = None
        if not auth or not auth['email'] or not auth['password']:
            return make_response((jsonify({"message":"Authorize with email and password"})), 401)
        if isinstance(auth['email'], int):
            return make_response((jsonify({"message":"Please input a string"})), 401)
        if auth['email'].strip() == '':
            return make_response(jsonify({'message':"You cannot send an empty string"}), 401)
        if isinstance(auth['password'],unicode):
            if auth['password'].strip() == '':
                return make_response(jsonify({'message':"You cannot send an empty string"}), 401)
        if '@' not in auth['email'][:-4]:
            return make_response((jsonify({"message":'''"@" is missing'''})), 401)
        if auth['email'].lower().endswith('.com') is False:
            return make_response((jsonify({"message":"Input a valid email"})), 401)
        repeat = [char for char in auth['email'] if char == '@']
        if len(repeat) > 1:
            return make_response((jsonify({"message":'''Repetition of "@" is not allowed'''})), 401)
        if len(auth['email'])>60:
            return make_response((jsonify({"message":"Email should be less than 60 characters"})), 401)
        return response


    def __repr__ (self):
        return "id:{} email:{} admin:{}".format(self.id, self.email, self.admin_status)
    
    def __str__(self):
        return "{}".format(self.email)

    def save(self):
        DB.session.add(self)
        
    def commit(self):
        DB.session.commit()
    #DB.create_all()
class Admin(DB.Model):
    __tablename__ = 'admin'
    id = DB.Column(DB.Integer, primary_key=True)
    email = DB.Column(DB.String(60), unique=True)
    user_id = DB.Column(DB.Integer)
    admin_status = DB.Column(DB.Boolean, default=True)
    meals = DB.relationship('Meal', backref='admin')
    menus = DB.relationship('Menu', backref='admin')
    
    def __repr__ (self):
        return "id:{} email:{} admin:{} user_id:{} meals:{}".format(self.id, self.email, self.admin_status, self.user_id, self.meals)
    
    def __str__(self):
        return "{}".format(self.email)

    def save(self):
        DB.session.add(self)
        
    def commit(self):
        DB.session.commit()

class Meal(DB.Model):
    __tablename__ = 'meal'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(60), nullable = False, unique = True)
    price = DB.Column(DB.Integer, nullable = False)
    admin_id = DB.Column(DB.Integer, DB.ForeignKey('admin.id'))
    menus = DB.relationship('Menu', backref='meal')

    @staticmethod
    def verify_meal():
        response = None
        name =request.get_json('name')['name']
        price = request.get_json('price')['price']
        characters= re.compile('[!#$%&*+-.^_`|~:<>,0-9]')
        if not name and not price:
            return make_response(jsonify({'message':"Please send a json object containing name and price"}), 401)
        if type(price) == unicode:
            try:
                map(int, price.split())
                #return make_response(jsonify({'message':"Please put in an integer"}), 401)
            except ValueError:
                return make_response(jsonify({'message':"Please put in an integer"}), 401)
        if type(name) != unicode:
            return make_response(jsonify({'message':"Please input a string"}), 401)
        if characters.match(name):
            return make_response(jsonify({'message':"None alpha-numeric input"}), 401)
        if name.strip() == '':
            return make_response(jsonify({'message':"You cannot have whitespaces"}), 401)

    def save(self):
        DB.session.add(self)

    def delete(self):
        DB.session.delete(self)
        
    def commit(self):
        DB.session.commit()

    def __repr__(self):
        return 'id:{} name:{} price:{} adminId:{}'.format(self.id, self.name, self.price, self.admin_id)
    
    def __str__(self):
        return 'id:{} '.format(self.id)

class Menu(DB.Model):
    __tablename__ = 'menu'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(60), nullable=False)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey('admin.id'))
    meal_id = DB.Column(DB.Integer, DB.ForeignKey('meal.id'))
    day = DB.Column(DB.String(40), default = datetime.datetime.today())
    orders = DB.relationship('Order', backref='menu')
    active = DB.Column(DB.String(20))

    def save(self):
        DB.session.add(self)

    def delete(self):
        DB.session.delete(self)
        
    def commit(self):
        DB.session.commit()

    def __repr__(self):
        return 'id:{} name:{} owner_id:{} meal_id:{} day:{}'.format(self.id, self.name, self.owner_id, self.meal_id,self.day)
    
    def __str__(self):
        return 'id:{} '.format(self.id)



class Order(DB.Model):
    __tablename__ = 'order'
    id = DB.Column(DB.Integer, primary_key=True)
    menu_name = DB.Column(DB.Integer, DB.ForeignKey('menu.name')) 
    meal_id = DB.Column(DB.Integer)
    admin_id = DB.Column(DB.Integer)
    time_created = DB.Column(DB.String)
    customer_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'))

    def save(self):
        DB.session.add(self)

    def delete(self):
        DB.session.delete(self)
        
    def commit(self):
        DB.session.commit()

    def __repr__(self):
        return "id:{} menu_id:{} customer_id:{}".format(self.id, self.menu_id, self.customer_id)

    def __str__(self):
        return "id:{}".format(self.id)

DB.create_all()
