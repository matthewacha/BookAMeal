import unittest
import json
import random
from api import APP, DB

def login(tester):
    emails=random.choice(['an@gl.com','me@il.com','dou@ail.com','cassan@m.com','d@d.com','amos@ml.com','jake@m.com','g@na.com'])
    tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='cj@de.com',
                                                        password='lantern')))
    tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email=emails,
                                                        password='lantern')))
    login = tester.post('api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email=emails,
                                                        password='lantern')))
    return login

class TestMenu(unittest.TestCase):
    def setUp(self):
        """run at the start of every test case"""
        self.tester = APP.test_client(self)
        DB.create_all()
        DB.session.commit()
    def tearDown(self):
        """run at the end of every test case"""
        DB.drop_all()

    def test_create_menu(self):
        """test that a meal can be added to a menu"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())

        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())
        #self.assertIn(u'Successfully added to menu', response.data)
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))
        #self.assertIn(u'Successfully added to menu', response.data)
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Chicken',
                                                        price=15000)),
                         headers = dict(K_access_token = result2['token']))
        responsev=self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(name='Special')),
                                  headers = dict(K_access_token =result2['token']))
        self.assertIn(u'Successfully added to menu', responsev.data)
        self.assertEqual(responsev.status_code, 201)

    def test_add_unique_meal_to_menu(self):
        """test that a meal option can be added only once to the menu"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(name='Special')),
                                  headers = dict(K_access_token =result2['token']))
        response=self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(name='Special')),
                                  headers = dict(K_access_token =result2['token']))
        self.assertIn(u'Meal option already exists in menu', response.data)
        self.assertEqual(response.status_code, 401)
        
    def test_get_menu(self):
        """test that a menu can be got"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())
        
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(name='Special')),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/menus/1',content_type='application/json',
        data = json.dumps(dict(name='Special')),
                         headers =dict(K_access_token = result2['token']))
        response=self.tester.get('/api/v2/menus/Special',
                                 headers =dict(K_access_token = result2['token']))
        rv = json.loads(response.data.decode())
        self.assertEqual(2, rv['Menu'][0]['meal_id'])

    def test_get_no_menu(self):
        """test that message is sent when menu does not exist"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())

        response=self.tester.get('/api/v2/menus/Chillax',
                                 headers =dict(K_access_token = result2['token']))
        rv = json.loads(response.data.decode())
        self.assertEqual(u"Menu does not exist", rv['message'])

    def test_delete_menu_item(self):
        """test that a meal can be deleted from a menu"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())
        
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = result2['token']))
        
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = result2['token']))
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Chicken',
                                                        price=15000)),
                         headers =dict(access_token = result2['token']))
        self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(name='Special')),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/menus/3',content_type='application/json',
        data = json.dumps(dict(name='Special')), headers =dict(access_token = result2['token']))
        response=self.tester.delete('/api/v2/menus/Special/2', headers =dict(K_access_token = result2['token']))
        self.assertIn(u'Successfully deleted from menu', response.data)
        self.assertEqual(response.status_code, 200)

    def test_fail_delete_menu_meal(self):
        """test that a non existent meal cannot be deleted from a menu"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())
        
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = result2['token']))
        
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = result2['token']))
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Chicken',
                                                        price=15000)),
                         headers =dict(access_token = result2['token']))
        self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(name='Special')),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/menus/3',content_type='application/json',
        data = json.dumps(dict(name='Special')), headers =dict(access_token = result2['token']))

        response=self.tester.delete('/api/v2/menus/Special/4', headers =dict(K_access_token = result['token']))
        self.assertIn(u'Meal does not exist', response.data)
        self.assertEqual(response.status_code, 404)

    def test_fail_delete_menu_item(self):
        """test that a meal cannot be deleted from a non existent menu"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())

        response=self.tester.delete('/api/v2/menus/Sunday/4', headers =dict(K_access_token = result['token']))
        self.assertIn(u'Menu does not exist', response.data)
        self.assertEqual(response.status_code, 404)    

if __name__=='__main__':
    unittest.main()#pragma:no cover
