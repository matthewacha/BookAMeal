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
    
class TestMeal(unittest.TestCase):
    def setUp(self):
        self.tester = APP.test_client(self)

    def test_create_meal(self):
        """test that a meal option can be succesfully added"""
        login_=login(self.tester)
        result = json.loads(login_.data.decode())
        response= self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                                   headers =dict(access_token = result['token']))
        #rest=json.loads(response.data.decode())
        self.assertIn(u'Successfully added meal option', response.data)
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_create_meal(self):
        """test that a meal option cannot be succesfully added"""
        response= self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                                   headers =dict(access_token = u'123456'))
        #rest=json.loads(response.data.decode())
        self.assertIn(u'Unauthorized access, please login', response.data)
        self.assertEqual(response.status_code, 401)



    def test_fail_create_meal(self):
        """test that a meal option cannot be added if strin price
        is passed instead of integer"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())
        response= self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price='anim45')),
                                   headers =dict(access_token = resv['token']))
        result=json.loads(response.data.decode())
        self.assertEqual(result['message'], u'Meal option already exists, try another')
        self.assertEqual(response.status_code, 401)

    def test_get_all_meals(self):
        """test that all meal options can be retrieved"""
        login_=login(self.tester)
        resv = json.loads(login_.data.decode())

        self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = resv['token']))
        self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = resv['token']))
        response=self.tester.get('api/v1/meals/',
                                 headers =dict(access_token = resv['token']))
        result=json.loads(response.data.decode())

        self.assertEqual(len(result['Meals']), 2)

    def test_update_meal(self):
        """test that a meal option can be updated"""
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
        
        response=self.tester.put('/api/v1/meals/1',content_type='application/json',
                                  data=json.dumps(dict(name='Beans n fries',
                                                       price=3500)),
                                 headers =dict(access_token = resv['token']))
        self.assertIn(u'Successfully updated meal', response.data)
        self.assertEqual(response.status_code, 201)

    def test_fail_update_meal(self):
        """test that a non existent meal option cannot be updated """
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
        response=self.tester.put('/api/v1/meals/3',content_type='application/json',
                                  data=json.dumps(dict(name='Beans fries',
                                                       price=4500)),
                                 headers =dict(access_token = resv['token']))
        self.assertIn(u'Meal option does not exist', response.data)
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
        """test that a non existent meal option cannot be deleted """
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
        response=self.tester.delete('/api/v1/meals/3',
                                    headers =dict(access_token = resv['token']))
        self.assertIn(u'Failed to delete meal', response.data)
        self.assertEqual(response.status_code, 401)
    
        

if __name__=='__main__':
    unittest.main()#pragma:no cover
