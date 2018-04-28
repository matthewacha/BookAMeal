import unittest
import json
from app import APP

def login(tester):
    tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
    login = tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
    return login

class TestMenu(unittest.TestCase):
    def setUp(self):
        self.tester = APP.test_client(self)

    def test_create_menu(self):
        """test that a meal can be added to a menu"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = result['token']))
        
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Chicken',
                                                        price=15000)),
                         headers =dict(access_token = result['token']))
        response=self.tester.post('/api/v1/menu/2',
                                  headers =dict(access_token = result['token']))
        self.assertIn(u'Successfully added to menu', response.data)
        self.assertEqual(response.status_code, 201)

    def test_unique_items_to_menu(self):
        """test that a meal option can be added only once to the menu"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/menu/2',
                         headers =dict(access_token = result['token']))
        response=self.tester.post('/api/v1/menu/2',
                                  headers =dict(access_token = result['token']))
        self.assertIn(u'Meal already exists in menu', response.data)
        
    def test_get_menu(self):
        """test that a menu can be got"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/menu/2',
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/menu/1',
                         headers =dict(access_token = result['token']))
        response=self.tester.get('/api/v1/menu/',
                                 headers =dict(access_token = result['token']))
        self.assertIn(u'Beans', response.data)

if __name__=='__main__':
    unittest.main()#pragma:no cover
