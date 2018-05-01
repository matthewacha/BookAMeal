import os
from flask import Flask, jsonify, request, session, make_response, abort
from flask_restful import Resource, Api
from flasgger.utils import swag_from
from app.models import database,meals_db, menu_db
from . import menus
from app.v1.users.views import token_required

menuapi=Api(menus)

class Resource(Resource):
    method_decorators=[token_required]

class menu(Resource):
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

    @swag_from('api-docs/delete_menu.yml')
    def delete(self, current_user, meal_id):
        menu_meal=[meal for meal in menu_db if meal['meal_id']==meal_id]
        if menu_meal:
            menu_meal.remove(menu_meal[0])
            return make_response(jsonify({"message":"Successfully deleted from menu"}), 200)
        return make_response(jsonify({"message":"Meal does not exist"}), 404)

class view_menu(Resource):
    @swag_from('api-docs/view_menu.yml')
    def get(self,current_user):
        return make_response((jsonify({"menu":menu_db})),201)

menuapi.add_resource(menu, 'menu/<int:meal_id>')
menuapi.add_resource(view_menu, 'menu/')
