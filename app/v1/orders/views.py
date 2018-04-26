import os
from flask import Flask, jsonify, request, session, make_response, abort
from flask_restful import Resource, Api
from app.models import database, menu_db, orders_db
from . import orders

orderapi=Api(orders)
class make_order(Resource):
    def post(self, meal_id):
        menu_meal=[meal for meal in menu_db if meal['meal_id']==meal_id]
        if len(menu_meal)>0:
            orders_db.append(menu_meal[0])
            return jsonify({"message":menu_meal[0]})
        return jsonify({"message":"Not successful, try again"})
    def put(self,meal_id):
        return jsonify({"message":"Successfully edited"})

class get_orders(Resource):
    def get(self):
        return jsonify({"orders":orders_db})
    
orderapi.add_resource(make_order,'orders/<int:meal_id>')
orderapi.add_resource(get_orders,'orders')
