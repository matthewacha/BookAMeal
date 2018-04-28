database = []
meals_db = []
menu_db = []
orders_db = []
class User(object):
    """Creates user object"""
    def __init__(self,email,password):
        self.email = email
        self.password = password

    def generate_id(self, number):
        """generates user id"""
        return number+1

class Meal(object):
    """Creates meal object"""
    def __init__(self, name, price,user_id):
        self.name = name
        self.price = price
        self.user_id = user_id

    def generate_id(self, number):
        """generates meal id"""
        return number+1