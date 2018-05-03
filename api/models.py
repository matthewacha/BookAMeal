from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from api import DB

class User(DB.Model):
    __tablename__ = 'user'
    id = DB.Column(DB.Integer, primary_key=True)
    email = DB.Column(DB.String(60), unique=True)
    password = DB.Column(DB.String(300))
    Admin_status = DB.Column(DB.Boolean, default=False)
    menus = DB.relationship('Menu', backref='user')
    orders = DB.relationship('Order', backref='user')
    
    def __repr__ (self):
        return "id:{} email:{} Admin:{}".format(self.id, self.email, self.Admin_status)
    
    def __str__(self):
        return "{}".format(self.email)

    def save(self):
        DB.session.add(self)
        
    def commit(self):
        DB.session.commit()

class Meal(DB.Model):
    __tablename__ = 'meals'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(60), nullable = False, unique = True)
    price = DB.Column(DB.Integer, nullable = False)
    Menu_meal_id = DB.Column(DB.Integer, DB.ForeignKey('menu_meal.id'))

    def save(self):
        DB.session.add(self)

    def delete(self):
        DB.session.delete(self)
        
    def commit(self):
        DB.session.commit()

    def __repr__(self):
        return 'id:{} name:{} price:{} menu_meal_id:{}'.format(self.id, self.name, self.price, self.Menu_meal_id)
    
    def __str__(self):
        return 'id:{} '.format(self.id)

class Menu(DB.Model):
    __tablename__ = 'menu'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(60), nullable=False, unique=True)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'))#Add foreign key here
    day = DB.Column(DB.String(60))
    Menu_meal_id = DB.Column(DB.Integer, DB.ForeignKey('menu_meal.id'))

    def save(self):
        DB.session.add(self)

    def delete(self):
        DB.session.delete(self)
        
    def commit(self):
        DB.session.commit()

    def __repr__(self):
        return 'id:{} name:{} owner_id:{} menu_meal_id:{} day:{}'.format(self.id, self.name, self.owner_id, self.Menu_meal_id,self.day)
    
    def __str__(self):
        return 'id:{} '.format(self.id)

class Menu_Meal(DB.Model):
    __tablename__ = 'menu_meal'
    id = DB.Column(DB.Integer, primary_key=True)
    menus = DB.relationship('Menu', backref='menu_meal')
    meals = DB.relationship('Meal', backref='menu_meal')

    def save(self):
        DB.session.add(self)

    def delete(self):
        DB.session.delete(self)
        
    def commit(self):
        DB.session.commit()

    def __repr__(self):
        return 'id:{}'.format(self.id)
    
    def __str__(self):
        return 'id:{} '.format(self.id)

class Order(DB.Model):
    __tablename__ = 'order'
    id = DB.Column(DB.Integer, primary_key=True)
    menu_id = DB.Column(DB.Integer, DB.ForeignKey('menu.id'))
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