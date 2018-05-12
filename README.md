__Book-A-Meal__ 
[![Build Status](https://travis-ci.org/matthewacha/BookAMeal.svg?branch=userEP)](https://travis-ci.org/matthewacha/BookAMeal) [![Coverage Status](https://coveralls.io/repos/github/matthewacha/BookAMeal/badge.svg?branch=userEP)](https://coveralls.io/github/matthewacha/BookAMeal?branch=userEP) [![Maintainability](https://api.codeclimate.com/v1/badges/0f81265250e64a32b7b3/maintainability)](https://codeclimate.com/github/matthewacha/BookAMeal/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/0f81265250e64a32b7b3/test_coverage)](https://codeclimate.com/github/matthewacha/BookAMeal/test_coverage)

__Description__

__Book_A_Meal__ is a web based app that enables caterers to setup 
menus,view customer orders and also check order history, revenues for specific days. Book_A_Meal also gives customers a platform to place orders based on items on the day's menu, change their orders, and also view theirorde history.

The app is built with ___python/Flask___ and ___React/Redux___ for the backend and frontend respectively

__How to setup the api backend__

___Prerequisites___

__For windows__

a. Git 

b. python 2.7 or higher

c. Install pip [here](https://pip.pypa.io/en/stable/installing/) 

d. To install virtual environment `pip install virtualenv` for 
python 2.x `pip3 install virtualenv`

e. To setup virtual environment `virtualenv env`

f. To activate virtual environment `env\Scripts\activate`

__For Linux__

Linux terminal comes with python preinstalled.

Check what version of python is installed `python -V`.

a. Install pip [here](https://pip.pypa.io/en/stable/installing/)

b. To install virtual environment `pip install virtualenv` for 
python 2.x `pip3 install virtualenv`

c. To setup virtual environment `source virtualenv env`

d. To activate virtual environment `source env/bin/activate`


1. Navigate to a folder in which you want to clone your repository. Clone the repository `git clone urlOfRepository` or download zip.

__for quick start__

2. Run the file setup.py `python setup.py` and follow the prompts for easy
start of server

__otherwise__

3. a. Activate the virtual environment. Then install dependencies `pip install -r requirements.txt`
   b. To run ___tests__ without coverage input `python manage.py test`
   
   c. To run tests with coverage input `python manage.py cover`
   
   d. To start the server input `python manage.py runserver`

__How to use the api__

The api has two versions running.

Navigate to the following endpoints in browser `127.0.0.1:5000/endpointUrl`

__For version_1__

|EndPoint|Functionality|
|---------|------------|
|[POST/api/v1/auth/signup](http://127.0.0.1:5000/apidocs/#!/User/post_api_v1_auth_signup)|Creates a user account|
|[POST/api/v1/auth/login](http://127.0.0.1:5000/apidocs/#!/User/post_api_v1_auth_login))|Logs in a user|
|[POST/api/v1/meals/](http://127.0.0.1:5000/apidocs/#!/Meal/post_api_v1_meals)|Caterer can add meal option|
|[GET/api/v1/meals/](http://127.0.0.1:5000/apidocs/#!/Meal/get_api_v1_meals)|Caterer can get all meal options added|
|[PUT/api/v1/meals/<meal_id>](http://127.0.0.1:5000/apidocs/#!/Meal/put_api_v1_meals_meal_id)|Caterer can update a meal|
|[DELETE/api/v1/meals/<meal_id>](http://127.0.0.1:5000/apidocs/#!/delete_api_v1_meals_meal_id)|Caterer can delete a meal|
|[POST/api/v1/menu/<meal_id>](http://127.0.0.1:5000/apidocs/#!/Meal/post_api_v1_menu_meal_id)|Caterer can add meal option to menu|
|[GET/api/v1/menu/](http://127.0.0.1:5000/apidocs/#!/Meal/get_api_v1_menu)|Caterer can get a menu|
|[DELETE/api/v1/menu/<meal_id>](http://127.0.0.1:5000/apidocs/#!/Meal/delete_api_v1_menu_meal_id)|Caterer can delete item from menu|
|[POST/api/v1/orders/<meal_id>](http://127.0.0.1:5000/apidocs/#!/Meal/post_api_v1_orders_meal_id)|Customer can make an order|
|[GET/api/v1/orders](http://127.0.0.1:5000/apidocs/#!/Meal/get_api_v1_orders)|Caterer can get all orders|
|[DELETE/api/v1/orders](http://127.0.0.1:5000/apidocs/#!/Meal/delete_api_v1_orders_meal_id)|Customer can delete an order|



For more about using the API check 127.0.0.1:5000/apidocs or [`https://bookameal.herokuapp.com/apidocs/`](https://bookameal.herokuapp.com/apidocs/)

__How setup api frontend__

__pre-requisites__

Download and install node.js

In the terminal navigate to the root folder of the react app in the repository.

'Install dependencies using bower'

'run server'

'browse urls'  

__Author:__

Wacha Opio Matthew
