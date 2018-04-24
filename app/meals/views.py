import os
from flask import Flask, jsonify, request, session, make_response, abort
from flask_restful import Resource, Api
from app.models import database,meals_db, Meal
from . import meals

mealapi=Api(meals)

class add_meal(Resource):
    def post(self):
        data = request.get_json()
        user_id=1#this is temporary
        if isinstance(data['price'],str):
            return make_response(jsonify({'message':"Please put in an integer"}),401)
        for meal in meals_db:
            if data['name']==meal['details'].name:
                return make_response(jsonify({'message':"Meal option already exists, try another"}),401)
        meal = Meal(data['name'],data['price'], user_id)
        meal_prof = {"details":meal,"meal_id":meal.generate_id(len(meals_db))}
        meals_db.append(meal_prof)
        return make_response(jsonify({'message':"Successfully added meal option"}),201)

    def get(self):
        data=request.get_json()
        list_meals=[]
        for meal in meals_db:
            output={}
            output['meal_name']=meal['details'].name
            output['meal_price']=meal['details'].price
            output['user_id']=meal['details'].user_id
            output['meal_id']=meal['meal_id']
            list_meals.append(output)
        return jsonify({"meals":list_meals})

mealapi.add_resource(add_meal, 'meals/')
