database=[]

class User():
    def __init__(self,email,password):
        self.email=email
        self.password=password

    def generate_id(self,number):
        return number+1

class Meal():
    def __init__(self, name, price):
        self.name=name
        self.price=price

class Order():
    def __init__(self, meal, price):
        self.meal=meal
        self.price=price
