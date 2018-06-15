import unittest
import json
import random
from api import APP, DB
emailx = ['an@gl.com','me@il.com','dou@ail.com','cassan@m.com','d@d.com','amos@ml.com','jake@m.com','g@na.com'] 
def login(tester):
    emails=random.choice(['an@gl.com','me@il.com','dou@ail.com','cassan@m.com','d@d.com','amos@ml.com','jake@m.com','g@na.com'])
    """tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='cj@de.com',
                                                        password='lantern')))"""
    tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email=emails,
                                                        password='lantern')))
    login = tester.post('api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email=emails,
                                                        password='lantern')))
    return login
    
class TestMeal(unittest.TestCase):
    def setUp(self):
        self.tester = APP.test_client(self)
        DB.create_all()
        DB.session.commit()
    def tearDown(self):
        DB.drop_all()


    def test_create_meal(self):
        """test that a meal option can be succesfully added"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())
        resp= self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Lobster',
                                                        price=5000)),
                                   headers =dict(K_access_token = result2['token']))
        self.assertIn(u'Successfully added meal option', resp.data)
        self.assertEqual(resp.status_code, 201)

    def test_token_missing_create_meal(self):
        """test that a meal option cannot be succesfully added with missing token"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        response= self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                                   headers =dict(access_token = result['token']))
        self.assertIn(u'Admin token is missing', response.data)
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_create_meal(self):
        """test that non authorized user cannot add meal"""

        response= self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                                                        headers =dict(K_access_token=u"55678764"))
        self.assertIn(u"Unauthorized access, please login as admin", response.data)
        self.assertEqual(response.status_code, 401)



    def test_fail_create_meal_unicode_price(self):
        """test that a meal option cannot be added if string price
        is passed instead of integer"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())
        response1= self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries and wine',
                                                        price='678addf')),
                                   headers =dict(K_access_token = result2['token']))
        result3=json.loads(response1.data.decode())
        self.assertEqual(result3['message'], u"Please put in an integer")
        self.assertEqual(response1.status_code, 401)

    def test_fail_create_meal_non_alpha_numeric_name(self):
        """test that a meal option cannot be added if non alpha-numeric name"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())

        response= self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='....',
                                                        price=4353465)),
                                   headers =dict(K_access_token = result2['token']))

        result=json.loads(response.data.decode())
        self.assertEqual(result['message'], u"None alpha-numeric input")
        self.assertEqual(response.status_code, 401)

    def test_fail_create_meal_whitespcae_name(self):
        """test that a meal option cannot be added if whitespace in name"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())

        response= self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name="    ",
                                                        price=4353465)),
                                   headers =dict(K_access_token = result2['token']))

        result=json.loads(response.data.decode())
        self.assertEqual(result['message'], u"You cannot have whitespaces")
        self.assertEqual(response.status_code, 401)

    def test_fail_create_meal_none_string_type_name(self):
        """test that a meal option cannot be added if name is not unicode string"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())

        response= self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name=345646,
                                                        price=4353465)),
                                   headers =dict(K_access_token = result2['token']))

        result=json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Please input a string")
        self.assertEqual(response.status_code, 401)

    def test_fail_create_meal_no_inputs(self):
        """test that a meal option cannot be added if no inputs sent"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())

        response= self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name="",
                                                        price="")),
                                   headers =dict(K_access_token = result2['token']))

        result=json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Please send a json object containing name and price")
        self.assertEqual(response.status_code, 401)

    def test_fail_create_unique_meal(self):
        """test that a meal option cannot be added if meal not unique"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())

        self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Friess',
                                                        price=4000)),
                         headers =dict(K_access_token = result2['token']))

        response = self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Friess',
                                                        price=4000)),
                         headers =dict(K_access_token = result2['token']))

        result=json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Meal already exists")
        self.assertEqual(response.status_code, 400)

    def test_get_all_meals(self):
        """test that all meal options can be retrieved"""
        self.tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email="jona@gmail.com",
                                                        password='lantern')))
        login = self.tester.post('api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email="jona@gmail.com",
                                                        password='lantern')))
        resv = json.loads(login.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())
        self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Friess',
                                                        price=4000)),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Pizza pepper',
                                                        price=7000)),
                         headers =dict(K_access_token = resv['token']))

        response=self.tester.get('api/v2/meals/',headers =dict(K_access_token = resv['token']))
        result=json.loads(response.data.decode())

        self.assertEqual(len(result['Meals']), 2)
        self.assertEqual(response.status_code, 200)

    def test_update_meal(self):
        """test that a meal option can be updated"""
        self.tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email="amos@gmail.com",
                                                        password='lantern')))
        login = self.tester.post('api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email="amos@gmail.com",
                                                        password='lantern')))
        resv = json.loads(login.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())
        self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Yorghut',
                                                        price=55000)),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fishes',
                                                        price=4500)),
                         headers =dict(K_access_token = result2['token']))
        response=self.tester.put('api/v2/meals/2', data =json.dumps( dict(name='Fries',
                                                        price=55000)),
                                                        headers =dict(K_access_token = resv['token']))
        result=json.loads(response.data.decode())

        self.assertEqual(result['message'], u"Successfully edited")
        self.assertEqual(response.status_code, 201)
        
        
    def test_fail_update_meal(self):
        """test that a non existent meal option cannot be updated """
        self.tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email="many@gmail.com",
                                                        password='lantern')))
        login = self.tester.post('api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email="many@gmail.com",
                                                        password='lantern')))
        resv = json.loads(login.data.decode())
        
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))
        response=self.tester.put('api/v2/meals/17', data =json.dumps( dict(name='Fries',
                                                        price=55000)),
                                                        headers =dict(K_access_token = result2['token']))
        self.assertIn(u'Meal option does not exist', response.data)
        self.assertEqual(response.status_code, 404)

    def test_fail_update_meal_non_authorized(self):
        """test that a non authorized user cannot add meal option cannot"""

        self.tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email="andrew@gmail.com",
                                                        password='lantern')))

        login = self.tester.post('api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email="andrew@gmail.com",
                                                        password='lantern')))
        response=self.tester.put('api/v2/meals/2', data =json.dumps( dict(name='Fries',
                                                        price=55000)),
                                                        headers =dict(K_access_token = u'223344'))
        self.assertIn(u"Unauthorized access, please login as admin", response.data)
        self.assertEqual(response.status_code, 401)
        
    def test_delete_meal(self):
        """test that a meal can be deleted """
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))
        response=self.tester.delete('/api/v2/meals/2',
                                    headers =dict(K_access_token = result2['token']))
       
        self.assertIn(u'Successfully deleted meal', response.data)
        self.assertEqual(response.status_code, 200)

    def test_fail_to_delete_non_existent_meal(self):
        """test that a non existent meal option can not be deleted by admin"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = resv['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = resv['token']))
        result2 = json.loads(response.data.decode())
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))

        response=self.tester.delete('/api/v2/meals/2',
                                    headers =dict(K_access_token = result2['token']))
       
        self.assertIn(u"Meal does not exist", response.data)
        self.assertEqual(response.status_code, 404)

    def test_fail_to_delete_meal(self):
        """test that a meal option can only be deleted by admin"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = resv['token']))
        self.tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = resv['token']))
        response=self.tester.delete('/api/v2/meals/34',
                                    headers =dict(K_access_token = u"576i8"))
        self.assertIn(u'Unauthorized access, please login as admin', response.data)
        self.assertEqual(response.status_code, 401)
    
        

if __name__=='__main__':
    unittest.main()#pragma:no cover
