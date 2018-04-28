"""Meals views"""
from flask import jsonify, request, make_response
from flask_restful import Resource, Api
from flasgger.utils import swag_from
from app.models import meals_db, Meal
from app.v1.users.views import token_required
from . import meals

mealapi = Api(meals)
SECRET_KEY = 'VX-4178-WD-3429-MZ-31'

class MealsCrud(Resource):
    @token_required
    @swag_from('api-docs/add_meal.yml')
    def post(self, current_user):
        data = request.get_json()
        user_id = 1#this is temporary
        if isinstance(data['price'], str):
            return make_response(jsonify({'message':"Please put in an integer"}), 401)
        for meal in meals_db:
            if data['name'] == meal['details'].name:
                return make_response(jsonify({'message':"Meal option already exists, try another"}), 401)
        meal = Meal(data['name'], data['price'], user_id)
        meal_prof = {"details":meal, "meal_id":meal.generate_id(len(meals_db))}
        meals_db.append(meal_prof)
        return make_response(jsonify({'message':"Successfully added meal option"}), 201)

    @token_required
    @swag_from('api-docs/get_meals.yml')
    def get(self, current_user):
        list_meals = []
        for meal in meals_db:
            output = {}
            output['meal_name'] = meal['details'].name
            output['meal_price'] = meal['details'].price
            output['user_id'] = meal['details'].user_id
            output['meal_id'] = meal['meal_id']
            list_meals.append(output)
        return jsonify({"Meals":list_meals})
class SingleMeal(Resource):
    @token_required
    @swag_from('api-docs/update_meal.yml')
    def put(self, current_user, meal_id):
        data = request.get_json()
        meal = [meal for meal in meals_db if meal['meal_id'] == meal_id]
        """
        if meal[0]["details"].user_id!=user_id:
            return make_response((jsonify({'message':"Youre not authorized to do this"})),404)"""
        if meal:
            if data['name']:
                meal[0]['details'].name = data['name']
            if data['price']:
                meal[0]['details'].price = data['price']
            return make_response((jsonify({'message':"Successfully updated meal"})), 201) 
        return make_response((jsonify({'message':"Meal option does not exist"})), 404)

    @token_required
    @swag_from('api-docs/delete_meal.yml')
    def delete(self, current_user, meal_id):
        """
        if meal[0]["details"].user_id!=user_id:
            return make_response((jsonify({'message':"Youre not authorized to do this"})),404)"""
        meal = [meal for meal in meals_db if meal['meal_id'] == meal_id]
        """
        if meal[0]["details"].user_id!=user_id:
            return make_response((jsonify({'message':"Youre not authorized to do this"})),404)"""
        if meal:
            meals_db.remove(meal[0])
            return make_response((jsonify({'message':"Successfully deleted meal"})), 200)
        return make_response((jsonify({'message':"Failed to delete meal"})), 401)

mealapi.add_resource(MealsCrud, 'meals/')
mealapi.add_resource(SingleMeal, 'meals/<int:meal_id>')
