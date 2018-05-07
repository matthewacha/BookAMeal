from flask import Flask, jsonify, request, make_response
import flask_restful
from flask_restful import Resource, Api
from flasgger.utils import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from api import APP, DB
from api.models import Meal, User, Menu, Order, Admin
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
                user=User.query.filter_by(id=data["sub"]).first()
                current_user=user
            except:
                return make_response((jsonify({"message":"Unauthorized access, please login"})),401)
            return funct(current_user, *args, **kwargs)
        return make_response((jsonify({"message":"Token is missing"})),401) 
    return verify_token

def admin_required(funct):
    @wraps(funct)
    def verify_token(*args, **kwargs):
        token = None
        if 'K_access_token' in request.headers:
            token = request.headers['K_access_token']
            try:
                data = jwt.decode(token, SECRET_KEY)
                admin=Admin.query.filter_by(id=data["sub"]).first()
                current_admin=admin
            except:
                return make_response((jsonify({"message":"Unauthorized access, please login"})),401)
            return funct(current_user, *args, **kwargs)
        return make_response((jsonify({"message":"Token is missing"})),401) 
    return verify_token
    
class signup(Resource):
    @swag_from('api-docs/signup.yml')
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
        user=User.query.filter_by(email=json_data['email'].lower()).first()

        if user:
            return make_response((jsonify({"message":"User already exists"})), 401)

        """Create object user"""
        new_user = User(email=json_data['email'], password=generate_password_hash(json_data['password']))

        """Add user to database"""
        DB.session.add(new_user)
        DB.session.commit()
        #DB.session.close()
        return make_response((jsonify({"message":"Successfully signed up"})), 201)
    
class login(Resource):
    @swag_from('api-docs/login.yml')
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
        user=User.query.filter_by(email=auth['email'].lower()).first()
        #return make_response((jsonify({"message":user.email})), 404)
        if not user:
            return make_response((jsonify({"message":"User does not exist"})), 404)
        if check_password_hash(user.password, auth['password']):
            token = jwt.encode({
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 0, minutes = 45),
                "iat": datetime.datetime.utcnow(),
                "sub": user.id}, SECRET_KEY, algorithm = 'HS256')
            return jsonify({'token':token})
        else:
            return make_response((jsonify({"message":"Authorize with correct password"})), 401)
        
class admin(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/changeAdmin.yml')
    def post(self, current_user):
        user=User.query.filter_by(id = current_user.id).first()
        admin_user = Admin.query.filter_by(user_id=current_user.id).first()
        if user:
            if not admin_user:
                new_admin = Admin(email = current_user.email, user_id = current_user.id, Admin_status=True)
                new_admin.save()
                new_admin.commit()
                return make_response((jsonify({"message":"User set to admin"})), 201)
            return make_response((jsonify({"message":"User is already admin"})), 201)
        return make_response((jsonify({"message":"User does not exist"})), 201)

class adminLogin(Resource): 
    method_decorators=[token_required]
    @swag_from('api-docs/checkAdmin.yml')
    def post(self,current_user):
        admin_user = Admin.query.filter_by(user_id=current_user.id).first()
        if admin_user:
            token = jwt.encode({
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 0, minutes = 45),
                "iat": datetime.datetime.utcnow(),
                "sub": admin_user.id}, SECRET_KEY, algorithm = 'HS256')
            return jsonify({'token':token})
        return make_response((jsonify({"Admin_status":"Sorry, you are not authorize"})), 401)

class MealsCrud(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/add_meal.yml')
    def post(self, current_user):
        data = request.get_json()
        if type(data['price']) == unicode:
            try:
                map(int, data['price'].split())
                return make_response(jsonify({'message':"Please put in an integer"}), 401)
            except ValueError, IndexError:
                return make_response(jsonify({'message':"Please put in an integer"}), 401)
        meal = Meal.query.filter_by(name=data['name']).first()

        if not meal:
            new_meal=Meal(name=data['name'], price=data['price'])
            try:
                DB.session.add(new_meal)
                DB.session.commit()
                meals_list=[]
                meals= Meal.query.all()
                for meal in meals:
                    output={}
                    output['name']=meal.name
                    output['price'] = meal.price
                    output['id'] = meal.id
                    output['menu_id'] = meal.Menu_meal_id
                    meals_list.append(output)
                return make_response(jsonify({"message":"Successfully added meal option"}), 201)
            except:
                return make_response(jsonify({"message":"Error occured try again"}), 401)
            DB.session.close()
        return make_response(jsonify({"message":"Meal already exists"}), 400)

    method_decorators=[token_required]
    @swag_from('api-docs/get_meals.yml')
    def get(self, current_user):
        meals= Meal.query.all()
        meals_list=[]
        for meal in meals:
            if meal.user_id == current_user.id:
                #return make_response(jsonify({"Meals":[meal.user_id,current_user.id]}), 200)
                output={}
                output['name']=meal.name
                output['price'] = meal.price
                output['id'] = meal.id
                output['menu_meal_id'] = meal.Menu_meal_id
                meals_list.append(output)
            #return make_response(jsonify({"Meals":[meal.user_id,current_user.id]}), 200)
        return make_response(jsonify({"Meals":meals_list}), 200)

class SingleMeal(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/update_meal.yml')
    def put(self, current_user, meal_id):

        pass 

    method_decorators=[token_required]
    @swag_from('api-docs/delete_meal.yml')
    def delete(self, current_user, meal_id):
        pass

class menu(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/add_menu.yml')
    def post(self, current_user,meal_id):
        pass

    method_decorators=[token_required]
    @swag_from('api-docs/delete_menu.yml')
    def delete(self, current_user, meal_id):
        pass

class view_menu(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/view_menu.yml')
    def get(self,current_user):
        pass

class make_order(Resource):
    @token_required
    @swag_from('api-docs/add_order.yml')
    def post(self, current_user, meal_id):
        pass

    @token_required
    @swag_from('api-docs/delete_order.yml')
    def delete(self,current_user,meal_id):
        pass


class get_orders(Resource):
    @token_required
    @swag_from('api-docs/view_orders.yml')
    def get(self,current_user):
        pass
    
BOOKAPI.add_resource(make_order,'/api/v1/orders/<int:meal_id>')
BOOKAPI.add_resource(get_orders,'/api/v1/orders')

BOOKAPI.add_resource(menu, '/api/v1/menu/<int:meal_id>')
BOOKAPI.add_resource(view_menu, '/api/v1/menu/')

BOOKAPI.add_resource(MealsCrud, '/api/v1/meals/')
BOOKAPI.add_resource(SingleMeal, '/api/v1/meals/<int:meal_id>')

BOOKAPI.add_resource(signup, '/api/v1/auth/signup')
BOOKAPI.add_resource(login, '/api/v1/auth/login')
BOOKAPI.add_resource(admin, '/api/v1/auth/Admin')
BOOKAPI.add_resource(adminLogin, '/api/v1/auth/adminLogin')
