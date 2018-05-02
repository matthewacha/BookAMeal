import os

def create_app(dev_state):
    if dev_state == 'Development':
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI=os.path.join(BASE_DIR,"postgresql://postgres:password@localhost/bookameal")
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = 'VX-4178-WD-3429-MZ-31'
    else:
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = 'VX-4178-WD-3429-MZ-31'

if __name__=='__main__':
    create_app('Development')