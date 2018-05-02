from flask import Flask, jsonify, request, make_response
import flask_restful
from flask_restful import Resource, Api
from flasgger.utils import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from api import APP
from api.models import Meal, User, database, menu_db, orders_db, meals_db
import jwt
import datetime
from functools import wraps

BOOKAPI=Api(APP)
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

class MealsCrud(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/add_meal.yml')
    def post(self, current_user):
        data = request.get_json()
        user_id = current_user["user_id"]
        if type(data['price']) == unicode:
            try:
                map(int, data['price'].split())
                return make_response(jsonify({'message':"Please put in an integer"}), 401)
            except ValueError, IndexError:
                return make_response(jsonify({'message':"Please put in an integer"}), 401)
        for meal in meals_db:
            if data['name'] == meal['details'].name:
                return make_response(jsonify({'message':"Meal option already exists, try another"}), 401)
        meal = Meal(data['name'], data['price'], user_id)
        meal_prof = {"details":meal, "meal_id":meal.generate_id(len(meals_db))}
        meals_db.append(meal_prof)
        return make_response(jsonify({'message':"Successfully added meal option"}), 201)

    method_decorators=[token_required]
    @swag_from('api-docs/get_meals.yml')
    def get(self, current_user):
        list_meals = []
        for meal in meals_db:
            if meal['details'].user_id == current_user['user_id']:
                output = {}
                output['meal_name'] = meal['details'].name
                output['meal_price'] = meal['details'].price
                output['user_id'] = meal['details'].user_id
                output['meal_id'] = meal['meal_id']
                list_meals.append(output)
        return jsonify({"Meals":list_meals})
class SingleMeal(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/update_meal.yml')
    def put(self, current_user, meal_id):
        meal = [meal for meal in meals_db if meal['meal_id'] == meal_id]
        if not meal:
            return make_response((jsonify({'message':"Meal option does not exist"})), 404)
        if meal[0]["details"].user_id!=current_user['user_id']:
            return make_response((jsonify({'message':"Youre not authorized to do this"})),404)
        if meal:
            meal[0]['details'].name = request.get_json('name', meal[0]['details'].name)
            meal[0]['details'].price = request.get_json('price',meal[0]['details'].price)
            return make_response((jsonify({'message':"Successfully edited"})), 201) 

    method_decorators=[token_required]
    @swag_from('api-docs/delete_meal.yml')
    def delete(self, current_user, meal_id):
        meal = []
        count = 0
        no_id = 0
        for meal in meals_db:
            if meal['meal_id'] == meal_id:
                if meal["details"].user_id == current_user['user_id']:
                    meals_db.remove(meal)
                    count+=1
            else:
                no_id+=1
        if count >0:
            return make_response((jsonify({'message':"Successfully deleted meal"})), 200)
        elif no_id>0:
            return make_response((jsonify({'message':"Youre not authorized to do this"})),401)

class menu(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/add_menu.yml')
    def post(self, current_user,meal_id):
        menu_meal=[meal for meal in menu_db if meal['meal_id']==meal_id]

        meal=[meal for meal in meals_db if meal['meal_id']==meal_id]
        if len(menu_meal)>0:
            return make_response(jsonify({"message":"Meal already exists in menu"}),401)
        else:
            menu_db.append({"meal_name":meal[0]['details'].name,
                            "meal_price":meal[0]['details'].price,
                            "meal_id":meal[0]['meal_id']})
            return make_response(jsonify({"message":"Successfully added to menu"}),201)

    method_decorators=[token_required]
    @swag_from('api-docs/delete_menu.yml')
    def delete(self, current_user, meal_id):
        menu_meal=[meal for meal in menu_db if meal['meal_id']==meal_id]
        if menu_meal:
            menu_meal.remove(menu_meal[0])
            return make_response(jsonify({"message":"Successfully deleted from menu"}), 200)
        return make_response(jsonify({"message":"Meal does not exist"}), 404)

class view_menu(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/view_menu.yml')
    def get(self,current_user):
        return make_response((jsonify({"menu":menu_db})),201)

class make_order(Resource):
    @token_required
    @swag_from('api-docs/add_order.yml')
    def post(self, current_user, meal_id):
        menu_meal=[meal for meal in menu_db if meal['meal_id']==meal_id]
        if len(menu_meal)>0:
            orders_db.append(menu_meal[0])
            return jsonify({"message":"Successfully placed order"})
        return jsonify({"message":"Not successful, try again"})

    @token_required
    @swag_from('api-docs/delete_order.yml')
    def delete(self,current_user,meal_id):
        for order in orders_db:
            if order["meal_id"]==meal_id:
                orders_db.remove(order)
                return jsonify({"message":"Successfully deleted"})
        return jsonify({"message":"Order does not exist"})


class get_orders(Resource):
    @token_required
    @swag_from('api-docs/view_orders.yml')
    def get(self,current_user):
        output=[]
        for order in orders_db:
            output.append(order)
        return jsonify({"orders":output})
    
BOOKAPI.add_resource(make_order,'/api/v1/orders/<int:meal_id>')
BOOKAPI.add_resource(get_orders,'/api/v1/orders')

BOOKAPI.add_resource(menu, '/api/v1/menu/<int:meal_id>')
BOOKAPI.add_resource(view_menu, '/api/v1/menu/')

BOOKAPI.add_resource(MealsCrud, '/api/v1/meals/')
BOOKAPI.add_resource(SingleMeal, '/api/v1/meals/<int:meal_id>')

BOOKAPI.add_resource(signup, '/api/v1/auth/signup')
BOOKAPI.add_resource(login, '/api/v1/auth/login')
BOOKAPI.add_resource(Admin, '/api/v1/auth/Admin')
