import os

def create_app(dev_state):
    if dev_state == 'Development':
        SQLALCHEMY_DATABASE_URI = "postgresql://matthewacha:password@localhost/BookAMeal"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = 'VX-4178-WD-3429-MZ-31'
        print('working....')
    else:
        SECRET_KEY = 'VX-4178-WD-3429-MZ-31'

if __name__=='__main__':
    create_app('Development')