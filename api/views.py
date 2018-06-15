from flask import Flask, jsonify, request, make_response
import flask_restful
from flask_restful import Resource, Api
from flasgger.utils import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from api import APP, DB
from api.models import Meal, User, Menu, Order, Admin
import jwt
import re
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
        return make_response((jsonify({"message":"Token is missing"})),404) 
    return verify_token

def admin_required(funct):
    @wraps(funct)
    def verify_token(*args, **kwargs):
        token = None
        if 'K_access_token' in request.headers:
            token = request.headers['K_access_token']
            try:
                data = jwt.decode(token, SECRET_KEY)
                adminUser=Admin.query.filter_by(id=data["sub"]).first()
                current_admin=adminUser
            except:
                return make_response((jsonify({"message":"Unauthorized access, please login as admin"})),401)
            return funct(current_admin, *args, **kwargs)
        return make_response((jsonify({"message":"Admin token is missing"})),401) 
    return verify_token


class signup(Resource):
    @swag_from('api-docs/signup.yml')
    def post(self):
        json_data = request.get_json()
        """Check that user is unique"""
        verify = User.verify_input()
        if verify:
            return verify
        user=User.query.filter_by(email=json_data['email'].lower()).first()

        if user:
            return make_response((jsonify({"message":"User already exists"})), 401)

        """Create object user"""
        new_user = User(email=json_data['email'], password=generate_password_hash(json_data['password']))

        """Add user to database"""
        new_user.save()
        new_user.commit()
        return make_response((jsonify({"message":"Successfully signed up"})), 201)
    
class login(Resource):
    @swag_from('api-docs/login.yml')
    def post(self):
        auth = request.get_json()
        verify = User.verify_input()
        if verify:
            return verify
        """Verify user in database and password matches"""
        user=User.query.filter_by(email=auth['email'].lower()).first()
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
                new_admin = Admin(email = current_user.email, user_id = current_user.id, admin_status=True)
                new_admin.save()
                new_admin.commit()
                return make_response((jsonify({"message":"User set to admin"})), 201)
            return make_response((jsonify({"message":"User is already admin"})), 401)

    method_decorators=[token_required]
    @swag_from('api-docs/changeAdmin.yml')
    def get(self, current_user):
        user=User.query.filter_by(id = current_user.id).first()
        admin_user = Admin.query.filter_by(user_id=current_user.id).first()
        if user:
            if not admin_user:
                return make_response((jsonify({"message":"Not admin"})), 404)
            return make_response((jsonify({"message":"Admin"})), 200)

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
        return make_response((jsonify({"message":"Sorry, you are not authorized"})), 401)

class MealsCrud(Resource):
    method_decorators=[admin_required]
    @swag_from('api-docs/add_meal.yml')
    def post(self, current_admin):
        data = request.get_json()
        response = Meal.verify_meal()
        if response:
            return response
        meal = Meal.query.filter_by(name=data['name'],admin_id=current_admin.id).first()

        if not meal:
            new_meal=Meal(name=data['name'], price=data['price'],admin_id=current_admin.id)
            DB.session.add(new_meal)
            DB.session.commit()
            return make_response(jsonify({"message":"Successfully added meal option"}), 201)
        return make_response(jsonify({"message":"Meal already exists"}), 400)

    method_decorators=[admin_required]
    @swag_from('api-docs/get_meals.yml')
    def get(self, current_admin):
        meals= Meal.query.filter_by(admin_id=current_admin.id).all()
        meals_list=[]
        for meal in meals:
            output={}
            output['name']=meal.name
            output['price'] = meal.price
            output['id'] = meal.id
            meals_list.append(output)
        return make_response(jsonify({"Meals":meals_list}), 200)

class SingleMeal(Resource):
    method_decorators=[admin_required]
    @swag_from('api-docs/update_meal.yml')
    def put(self, current_admin, meal_id):
        response = Meal.verify_meal()
        if response:
            return response
        meal= Meal.query.filter_by(admin_id=current_admin.id, id=meal_id).first()
        if meal:
            meal.name = request.get_json('name')['name']
            meal.price = request.get_json('price')['price']
            meal.commit()
            return make_response(jsonify({"message":"Successfully edited"}), 201)
        return make_response(jsonify({"message":"Meal option does not exist"}), 404)

    method_decorators=[admin_required]
    @swag_from('api-docs/update_meal.yml')#fix this
    def get(self, current_admin, meal_id):
        meal= Meal.query.filter_by(admin_id=current_admin.id, id=meal_id).first()
        if meal:
            returnMeal={}
            returnMeal["name"] = meal.name
            returnMeal["price"] = meal.price
            return make_response(jsonify({"Meal":returnMeal}), 200)
        return make_response(jsonify({"message":"Meal option does not exist"}), 404)

    method_decorators=[admin_required]
    @swag_from('api-docs/delete_meal.yml')
    def delete(self, current_admin, meal_id):
        meals= Meal.query.filter_by(admin_id=current_admin.id).all()
        if meals:
            for meal in meals:
                if meal.id == meal_id:
                    DB.session.delete(meal)
                    DB.session.commit()
                    return make_response(jsonify({"message":"Successfully deleted meal"}), 200)
        return make_response(jsonify({"message":"Meal does not exist"}), 404)

class MenuCrud(Resource):
    method_decorators=[admin_required]
    @swag_from('api-docs/add_menu.yml')
    def post(self,current_admin, meal_id):
        data = request.get_json()
        menu_meal = Menu.query.filter_by(name=data['menu_name'], meal_id=meal_id).first()
        
        if menu_meal:
            return make_response(jsonify({"message":"Meal option already exists in menu"}), 401)
        else:
            menu_item = Menu(name=data['menu_name'], owner_id=current_admin.id,meal_id=meal_id,day=datetime.datetime.today().strftime('%d.%m.%y'),active="false")
            menu_item.save()
            menu_item.commit()
            return make_response(jsonify({"message":"Successfully added to menu"}), 201)
        
class delMenu(Resource):        
    method_decorators=[admin_required]
    @swag_from('api-docs/delete_menu.yml')
    def delete(self, current_user,meal_id, menu_name):
        menu = Menu.query.filter_by(name=menu_name).first()
        if menu:
            menu_meal = Menu.query.filter_by(name=menu_name, meal_id=meal_id).first()
            if menu_meal:
                menu_meal.delete()
                menu_meal.commit()
                return make_response(jsonify({"message":"Successfully deleted from menu"}), 200)
            else:
                return make_response(jsonify({"message":"Meal does not exist"}), 404)
        else:
            return make_response(jsonify({"message":"Menu does not exist"}), 404)
        

class view_menu(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/view_menu.yml')
    def get(self,current_user,menu_name):
        menu_list=[]
        menus=Menu.query.filter_by(name=menu_name).all()
        if menus:#should turn all items state to active for customers to know which menu is active
            for item in menus:
                output={}
                output['state'] = item.active
                output['id'] = item.id
                output['name'] = item.name
                output['admin_id'] = item.owner_id
                output['meal_id'] = item.meal_id
                output['Day'] = item.day
                menu_list.append(output)
            return make_response(jsonify({"Menu":menu_list}), 201)
        return make_response(jsonify({"message":"Menu does not exist"}), 404)

    method_decorators=[admin_required]
    @swag_from('api-docs/view_menu.yml')##
    def put(self,current_admin,menu_name):
        menus=Menu.query.filter_by(name=menu_name).all()
        if menus:
            for item in menus:
                item.active = request.get_json('state')['state']
                item.commit()
            return make_response(jsonify({"message":request.get_json()['state']}), 201)
        return make_response(jsonify({"message":"Menu does not exist"}), 404)



class Menus(Resource):
    method_decorators=[admin_required]
    @swag_from('api-docs/view_menu.yml')
    def get(self,current_admin):
        menus=Menu.query.filter_by(owner_id=current_admin.id).all()
        menus_list=[item.name for item in menus]
        unique_menus=set(menus_list)
        final_menus=list(unique_menus)
        return make_response(jsonify({"Menus":final_menus}), 201)

class ActiveMenu(Resource):
    method_decorators=[admin_required]
    @swag_from('api-docs/view_menu.yml')
    def get(self,current_admin):
        menu_meals=Menu.query.filter_by(owner_id=current_admin.id, active="true").all()
        menu_list=[]
	if menuMeals:
	    for meanu_meal in menu_meals:
		output={}
		output['state'] = meanu_meal.active
                output['id'] = meanu_meal.id
                output['name'] = menu_meal.name
                output['admin_id'] = menu_meal.owner_id
                output['meal_id'] = menu_meal.meal_id
                output['Day'] = menu_meal.day
		menu_list.append(output)

        return make_response(jsonify({"Menu":menu_list}), 201)


class make_order(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/add_order.yml')
    def post(self, current_user, menu_name, meal_id):
        menus=Menu.query.filter_by(name=menu_name).first()
        if menus:
            menu_meal = Menu.query.filter_by(name=menu_name, meal_id=meal_id).first()
            if menu_meal:
                order =Order(menu_name=menu_name,meal_id= meal_id, admin_id =menu_meal.owner_id, time_created = datetime.datetime.today().strftime('%d.%m.%y %H.%M.%S'),customer_id = current_user.id)
                order.save()
                order.commit()
                return make_response(jsonify({"message":"Order sent"}), 201)
            else:
                return make_response(jsonify({"message":"Meal does not exist in menu"}), 404)
        else:
            return make_response(jsonify({"message":"Menu does not exist"}), 404)


class userDeleteOrder(Resource):
    method_decorators=[token_required]
    def delete(self, current_user, order_id):
        """User deletes order"""
        order = Order.query.filter_by(customer_id = current_user.id, id = order_id).first()
        if order:
            order.delete()
            order.commit()
            return make_response(jsonify({"message":"Successfully deleted"}), 200)
        return make_response(jsonify({"message":"Order does not exist"}), 404)

class userOrders(Resource):
    method_decorators=[token_required]
    @swag_from('api-docs/view_orders.yml')
    def get(self,current_user, menu_name):
        """gets orders a user makes from a certain menu"""
        orders = Order.query.filter_by(customer_id = current_user.id).all()
        if orders:
            all_orders = []
            for order in orders:
                output={}
                output['menu_name'] = order.menu_name
                output['mealId'] = order.meal_id
                output['adminId'] = order.admin_id
                output['when'] = order.time_created
                output['customerId'] = order.customer_id
                output['orderId'] = order.id
                all_orders.append(output)
            return make_response(jsonify({"Orders":all_orders}), 200)

class adminGetOrders(Resource):
    method_decorators=[admin_required]
    @swag_from('api-docs/view_orders.yml')
    def get(self,current_admin):
        """gets all orders made by users from a menu of an admin"""
        orders = Order.query.filter_by(admin_id = current_admin.id).all()
        all_orders = []
        if orders:
            for order in orders:
                output={}
                output['menuName'] = order.menu_name
                output['mealId'] = order.meal_id
                output['adminId'] = order.admin_id
                output['when'] = order.time_created
                output['customerId'] = order.customer_id
                output['orderId'] = order.id
                all_orders.append(output)
        return make_response(jsonify({"Orders":all_orders}), 200)
    
BOOKAPI.add_resource(make_order,'/api/v2/orders/<menu_name>/<int:meal_id>')
BOOKAPI.add_resource(userDeleteOrder,'/api/v2/orders/<int:order_id>')
BOOKAPI.add_resource(userOrders,'/api/v2/orders/<menu_name>')
BOOKAPI.add_resource(adminGetOrders,'/api/v2/orders/admin')

BOOKAPI.add_resource(MenuCrud, '/api/v2/menus/<int:meal_id>')
BOOKAPI.add_resource(Menus, '/api/v2/menus/')
BOOKAPI.add_resource(ActiveMenu, '/api/v2/menu/')
BOOKAPI.add_resource(view_menu, '/api/v2/menus/<menu_name>')
BOOKAPI.add_resource(delMenu, '/api/v2/menus/<menu_name>/<int:meal_id>')

BOOKAPI.add_resource(MealsCrud, '/api/v2/meals/')
BOOKAPI.add_resource(SingleMeal, '/api/v2/meals/<int:meal_id>')

BOOKAPI.add_resource(signup, '/api/v2/auth/signup')
BOOKAPI.add_resource(login, '/api/v2/auth/login')
BOOKAPI.add_resource(admin, '/api/v2/auth/Admin')
BOOKAPI.add_resource(adminLogin, '/api/v2/auth/adminLogin')
