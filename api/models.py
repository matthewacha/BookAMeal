from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from api import DB

class User(DB.Model):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    email = DB.Column(DB.String(60), unique=True)
    password = DB.Column(DB.String(300))
    Admin_status = DB.Column(DB.Boolean, default=False)
    meals = DB.relationship('Meal', backref='user', lazy='dynamic')
    menus = DB.relationship('Menu', backref='user', lazy='dynamic')
    orders = DB.relationship('Order', backref='user', lazy='dynamic')
    def __init__ (self, email, password):
        self.email = email
        self.password = password
        DB.create_all()

class Meal(DB.Model):
    __tablename__ = 'meals'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(60), nullable=False, unique=True)
    price = DB.Column(DB.Integer, nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    def __init__ (self, name, price):
        self.name = name
        self.price = price
        DB.create_all()

class Menu(DB.Model):
    __tablename__ = 'menus'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(60), nullable=False, unique=True)
    price = DB.Column(DB.Integer, nullable=False)
    meal_id = DB.Column(DB.Integer)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    def __init__ (self, name, price):
        self.name = name
        self.price = price
        DB.create_all()

class Order(DB.Model):
    __tablename__ = 'orders'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(60), nullable=False, unique=True)
    price = DB.Column(DB.Integer, nullable=False)
    meal_id = DB.Column(DB.Integer)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    def __init__ (self, name, price):
        self.name = name
        self.price = price
        DB.create_all()