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
    
    def __repr__ (self):
        return "id:{} email:{} Admin:{}".format(self.id, self.email, self.Admin_status)
    
    def __str__(self):
        return "{}".format(self.email)

    def save(self):
        DB.session.add(self)
        
    def commit(self):
        DB.session.commit()

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
    admin_id = DB.Column(DB.Integer, DB.ForeignKey('admin.id'))
    Menus = DB.relationship('Menu', backref='meal')
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
    mealId = DB.Column(DB.Integer, DB.ForeignKey('meal.id'))
    day = DB.Column(DB.String, default = datetime.datetime.today())
    orders = DB.relationship('Order', backref='menu')

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

"""class Menu_Meal(DB.Model):
    __tablename__ = 'menu_meal'
    id = DB.Column(DB.Integer, primary_key=True)
    meal_id = DB.Column(DB.Integer, DB.ForeignKey('meal.id'))
    menus = DB.relationship('Menu', backref='menu_meal')
    #meals = DB.relationship('Meal', backref='menu_meal')

    def save(self):
        DB.session.add(self)

    def delete(self):
        DB.session.delete(self)
        
    def commit(self):
        DB.session.commit()

    def __repr__(self):
        return 'id:{}'.format(self.id)
    
    def __str__(self):
        return 'id:{} '.format(self.id)"""

class Order(DB.Model):
    __tablename__ = 'order'
    id = DB.Column(DB.Integer, primary_key=True)
    menu_id = DB.Column(DB.Integer, DB.ForeignKey('menu.name'))
    #time_created = DB.Column(DB.String, datetime.datetime.today().strftime('%d'))
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