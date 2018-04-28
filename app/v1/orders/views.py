import os
from flask import Flask, jsonify, request, session, make_response, abort
from flask_restful import Resource, Api
from flasgger.utils import swag_from
from app.models import database, menu_db, orders_db
from . import orders
from app.v1.users.views import token_required

SECRET_KEY = 'VX-4178-WD-3429-MZ-31'
orderapi=Api(orders)
current_orders=[]
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

    @token_required
    def put(self,current_user, meal_id):
        return jsonify({"message":"Successfully edited"})

class get_orders(Resource):
    @token_required
    @swag_from('api-docs/view_orders.yml')
    def get(self,current_user):
        output=[]
        for order in orders_db:
            output.append(order)
        return jsonify({"orders":output})
    
orderapi.add_resource(make_order,'orders/<int:meal_id>')
orderapi.add_resource(get_orders,'orders')
