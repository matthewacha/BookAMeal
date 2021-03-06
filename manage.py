"""Import dependencies"""
import unittest
import os
from flask_script import Manager
from app import APP

# create an instance of class that will handle our commands
MANAGER = Manager(APP)

"""define our command for testing called "test"
Usage: python manage.py test"""
@MANAGER.command
def run_test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
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
    APP.run(debug=True)

if __name__ == '__main__':
    MANAGER.run()
