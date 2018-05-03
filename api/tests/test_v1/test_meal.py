import unittest
import json
import random
from api import APP, DB

def login(tester):
    emails=random.choice(['an@gmail.com','me@gmail.com','dou@gmail.com'])
    tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email=emails,
                                                        password='lantern')))
    login = tester.post('api/v1/auth/login',content_type='application/json',
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
        response= self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Lobster',
                                                        price=5000)),
                                   headers =dict(access_token = result['token']))
        self.assertIn(u'Successfully added meal option', response.data)
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_create_meal(self):
        """test that a meal option cannot be succesfully added"""
        response= self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                                   headers =dict(access_token = u'123456'))
        self.assertIn(u'Unauthorized access, please login', response.data)
        self.assertEqual(response.status_code, 401)

        response= self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                                                        headers =dict())
        self.assertIn(u"Token is missing", response.data)
        self.assertEqual(response.status_code, 401)



    def test_fail_create_meal(self):
        """test that a meal option cannot be added if string price
        is passed instead of integer"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        response= self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries and wine',
                                                        price='678addf')),
                                   headers =dict(access_token = resv['token']))
        result=json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Please put in an integer")
        self.assertEqual(response.status_code, 401)

        response= self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries and wine',
                                                        price='67800')),
                                   headers =dict(access_token = resv['token']))

        result=json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Please put in an integer")
        self.assertEqual(response.status_code, 401)

    def test_get_all_meals(self):
        """test that all meal options can be retrieved"""
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email="jona@gmail.com",
                                                        password='lantern')))
        login = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email="jona@gmail.com",
                                                        password='lantern')))
        resv = json.loads(login.data.decode())
        self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Friess',
                                                        price=4000)),
                         headers =dict(access_token = resv['token']))
        self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Pizza pepper',
                                                        price=7000)),
                         headers =dict(access_token = resv['token']))

        response=self.tester.get('api/v1/meals/',headers =dict(access_token = resv['token']))
        result=json.loads(response.data.decode())

        self.assertEqual(result["Meals"], 2)

    def test_update_meal(self):
        """test that a meal option can be updated"""
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email="amos@gmail.com",
                                                        password='lantern')))
        login = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email="amos@gmail.com",
                                                        password='lantern')))
        resv = json.loads(login.data.decode())
        self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Yorghut',
                                                        price=55000)),
                         headers =dict(access_token = resv['token']))
        self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fishes',
                                                        price=4500)),
                         headers =dict(access_token = resv['token']))
        response=self.tester.put('api/v1/meals/6', data =json.dumps( dict(name='Fries',
                                                        price=55000)),
                                                        headers =dict(access_token = resv['token']))
        result=json.loads(response.data.decode())

        self.assertEqual(result['message'], "Successfully edited")
        
        
    def test_fail_update_meal(self):
        """test that a non existent meal option cannot be updated """
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email="many@gmail.com",
                                                        password='lantern')))
        login = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email="many@gmail.com",
                                                        password='lantern')))
        resv = json.loads(login.data.decode())
        
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = resv['token']))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = resv['token']))
        response=self.tester.put('api/v1/meals/17', data =json.dumps( dict(name='Fries',
                                                        price=55000)),
                                                        headers =dict(access_token = resv['token']))
        self.assertIn(u'Meal option does not exist', response.data)
        self.assertEqual(response.status_code, 404)

        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email="andrew@gmail.com",
                                                        password='lantern')))

        login = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email="andrew@gmail.com",
                                                        password='lantern')))
        resv = json.loads(login.data.decode())
        response=self.tester.put('api/v1/meals/2', data =json.dumps( dict(name='Fries',
                                                        price=55000)),
                                                        headers =dict(access_token = resv['token']))
        self.assertIn(u"Youre not authorized to do this", response.data)
        self.assertEqual(response.status_code, 404)
        
    def test_delete_meal(self):
        """test that a meal can be deleted """
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = resv['token']))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = resv['token']))
        response=self.tester.delete('/api/v1/meals/2',
                                    headers =dict(access_token = resv['token']))
       
        self.assertIn(u'Successfully deleted meal', response.data)
        self.assertEqual(response.status_code, 200)

    def test_fail_to_delete_meal(self):
        """test that a meal option can only be deleted by admin"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = resv['token']))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = resv['token']))
        response=self.tester.delete('/api/v1/meals/34',
                                    headers =dict(access_token = resv['token']))
        self.assertIn(u'Youre not authorized to do this', response.data)
        self.assertEqual(response.status_code, 401)
    
        

if __name__=='__main__':
    unittest.main()#pragma:no cover
