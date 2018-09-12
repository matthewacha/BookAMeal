"""Import dependencies"""
import unittest
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api import APP, DB

# create an instance of class that will handle our commands
MANAGER = Manager(APP)

MIGRATE = Migrate(APP, DB)

MANAGER.add_command('DB', MigrateCommand)

"""define our command for testing called "test"
Usage: python manage.py test"""
@MANAGER.command
def run_test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('api/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@MANAGER.command
def cover():
    """runs the unit tests with coverage"""
    os.system('coverage run manage.py run_test')
    os.system('coverage report')
    os.system('coverage html')

@MANAGER.command
def run_app():
    """Starts the server and debugs with the shell"""
    
    APP.run(host='bookameal1.herokuapp.com', debug=True)
port = os.getenv('PORT', 8322)
host = os.getenv('HOST')
application = APP.run(host=host, port = port, debug=False)
if __name__ == '__main__':
    MANAGER.run()
