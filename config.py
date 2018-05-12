import os

def create_app(dev_state):
    if dev_state == 'Development':
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/bookameal"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = 'VX-4178-WD-3429-MZ-31'
    else:
        SECRET_KEY = 'VX-4178-WD-3429-MZ-31'

if __name__=='__main__':
    create_app('Dev')