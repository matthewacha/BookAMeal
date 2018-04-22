#Book-A-Meal#

__Description__

__Book_A_Meal__ is a web based app that enables caterers to setup 
menus,view customer orders and also check order history, revenues for specific days. Book_A_Meal also gives customers a platform to place orders based on items on the day's menu, change their orders, and also view theirorde history.

The app is built with ___python/Flask___ and ___React/Redux___ for the backend and frontend respectively

__How to setup the api backend__

___Prerequisites___

__For windows__

a. Git 

b. python 2.7 or higher

c. Install pip `pip address` or easyinstall `easy address`

d. To install virtual environment `pip install virtualenv` for 
python 2.x `pip3 install virtualenv`

e. To setup virtual environment `virtualenv env`

f. To activate virtual environment `env\Scripts\activate`

__For ubuntu__

Linux terminal comes with python preinstalled.

Check what version of python is installed `python -V`.

a. Install pip `pip address` or easyinstall `easy address`

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
|[POST/api/v1/auth/register](#)|Creates a user account|
|[POST/api/v1/auth/login](#))|Logs in a user|
|[POST/api/v1/auth/logout](#)|Logs out a user|


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
