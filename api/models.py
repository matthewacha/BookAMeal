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
    Admin_status = DB.Column(DB.Boolean, default=False)
    orders = DB.relationship('Order', backref='user')
    def __init__(self,email,password,Admin_status=False):
        self.email = email
        self.password = password
        self.Admin_status = Admin_status

    def __repr__ (self):
        return "id:{} email:{} Admin:{}".format(self.id, self.email, self.Admin_status)
    
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
    Admin_status = DB.Column(DB.Boolean, default=True)
    meals = DB.relationship('Meal', backref='admin')
    menus = DB.relationship('Menu', backref='admin')
    
    def __repr__ (self):
        return "id:{} email:{} Admin:{} user_id:{} meals:{}".format(self.id, self.email, self.Admin_status, self.user_id, self.meals)
    
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
    adminId = DB.Column(DB.Integer, DB.ForeignKey('admin.id'))
    menus = DB.relationship('Menu', backref='meal')

    def verify_meal(self):
        response = None
        characters= re.compile('[!#$%&*+-.^_`|~:<>,0-9]')
        if not self.name and not self.price:
            return make_response(jsonify({'message':"Please send a json object containing name and price"}), 401)
        if type(self.price) == unicode:
            try:
                map(int, self.price.split())
                #return make_response(jsonify({'message':"Please put in an integer"}), 401)
            except ValueError:
                return make_response(jsonify({'message':"Please put in an integer"}), 401)
        if type(self.name) != unicode:
            return make_response(jsonify({'message':"Please input a string"}), 401)
        if characters.match(self.name):
            return make_response(jsonify({'message':"None alpha-numeric input"}), 401)
        if self.name.strip() == '':
            return make_response(jsonify({'message':"You cannot have whitespaces"}), 401)

    def save(self):
        DB.session.add(self)

    def delete(self):
        DB.session.delete(self)
        
    def commit(self):
        DB.session.commit()

    def __repr__(self):
        return 'id:{} name:{} price:{} adminId:{}'.format(self.id, self.name, self.price, self.adminId)
    
    def __str__(self):
        return 'id:{} '.format(self.id)

class Menu(DB.Model):
    __tablename__ = 'menu'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(60), nullable=False)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey('admin.id'))
    mealId = DB.Column(DB.Integer, DB.ForeignKey('meal.id'))
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
        return 'id:{} name:{} owner_id:{} mealId:{} day:{}'.format(self.id, self.name, self.owner_id, self.mealId,self.day)
    
    def __str__(self):
        return 'id:{} '.format(self.id)



class Order(DB.Model):
    __tablename__ = 'order'
    id = DB.Column(DB.Integer, primary_key=True)
    menuName = DB.Column(DB.Integer, DB.ForeignKey('menu.name')) 
    mealId = DB.Column(DB.Integer)
    adminId = DB.Column(DB.Integer)
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
