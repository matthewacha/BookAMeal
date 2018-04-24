import os
from flask import Flask, jsonify, request, session, make_response, abort
from flask_restful import Resource, Api
from app.models import database,meals_db, Meal
from . import meals

mealapi=Api(meals)

class meals(Resource):
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
    
class single_meal(Resource):
    def put(self,meal_id):
        data= request.get_json()
        prev_meal=[]
        
        Idlist = map(int, meal_id.split())
        meal_id = Idlist[0]
        
        for meal in meals_db:
            if meal['meal_id']==meal_id:
                output={}
                output['meal_name']=meal['details'].name
                output['meal_price']=meal['details'].price
                output['user_id']=meal['details'].user_id
                output['meal_id']=meal['meal_id']
                prev_meal.append(output)

        meal=[meal for meal in meals_db if meal['meal_id']==meal_id]
        if len(meal)>0:
            meal['details'].name=data['name']
            meal['details'].price=data['price']
            return make_response((jsonify({'message':"Successfully updated meal option"})),201) 
        return make_response((jsonify({'message':"Failed to edit"})),401)

mealapi.add_resource(meals, 'meals/')
mealapi.add_resource(single_meal, 'meals/<meal_id>')
