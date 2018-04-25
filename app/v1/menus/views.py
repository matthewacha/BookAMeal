import os
from flask import Flask, jsonify, request, session, make_response, abort
from flask_restful import Resource, Api
from app.models import database,meals_db
from . import menus

menuapi=Api(menus)
menu_db=[]

class menu(Resource):
    def post(self, meal_id):
        menu_meal=[meal for meal in menu_db if meal['meal_id']==meal_id]

        meal=[meal for meal in meals_db if meal['meal_id']==meal_id]
        if len(menu_meal)>0:
            return make_response(jsonify({"message":"Meal already exists in menu"}),401)
        else:
            menu_db.append({"meal_name":meal[0]['details'].name,
                            "meal_price":meal[0]['details'].price,
                            "meal_id":meal[0]['meal_id']})
            return make_response(jsonify({"message":"Successfully added to menu"}),201)

class view_menu(Resource):
    def get(self):
        return make_response((jsonify({"menu":menu_db})),201)

menuapi.add_resource(menu, 'menu/<int:meal_id>')
menuapi.add_resource(view_menu, 'menu/')
