import unittest
import json
from api import APP

def login(tester):
    tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail.com',
                                                        password='lantern')))
    login = tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail.com',
                                                        password='lantern')))
    result = json.loads(login.data.decode())
    return result

def add_meal(tester, result):
    tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(access_token = result['token']))
    tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(access_token = result['token']))
    response=tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Chicken',
                                                        price=15000)),
                         headers =dict(access_token = result['token']))
    return response

class TestOrders(unittest.TestCase):
    def setUp(self):
        self.tester = APP.test_client(self)
        
    def test_make_order(self):
        """test that a customer can make an order"""
        result=login(self.tester)
        add_meal(self.tester,result)
        
        """post to day's menu"""
        self.tester.post('/api/v1/menu/1',
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/menu/2',
                         headers =dict(access_token = result['token']))

        #make an order
        self.tester.post('/api/v1/orders/1',
                                  headers =dict(access_token = result['token']))
        response=self.tester.post('/api/v1/orders/2',
                                  headers =dict(access_token = result['token']))
        self.assertIn(u"Successfully placed order", response.data)

    def test_fail_make_order(self):
        """test that a customer cannot make an order"""
        result=login(self.tester)
        add_meal(self.tester,result)
        
        """post to day's menu"""
        self.tester.post('/api/v1/menu/1',
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/menu/2',
                         headers =dict(access_token = result['token']))

        #make an order
        self.tester.post('/api/v1/orders/1',
                                  headers =dict(access_token = result['token']))
        response=self.tester.post('/api/v1/orders/4',
                                  headers =dict(access_token = result['token']))
        self.assertIn(u"Not successful, try again", response.data)

    def test_get_all_orders(self):
        """test that a customer can get all orders from menu"""
        result=login(self.tester)
        add_meal(self.tester,result)
        #add meals to menu
        self.tester.post('/api/v1/menu/3',
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/menu/2',
                         headers =dict(access_token = result['token']))
        
        self.tester.post('/api/v1/orders/3',
                                  headers =dict(access_token = result['token']))
        #orders 
        self.tester.post('/api/v1/orders/2',
                                  headers =dict(access_token = result['token']))
        
        responsev=self.tester.get('/api/v1/orders',
                                  headers =dict(access_token = result['token']))

        self.assertIn(u"Beans", responsev.data)

    def test_delete_orders(self):
        """tests that an order can be deleted"""
        result=login(self.tester)
        add_meal(self.tester,result)
        #add meals to menu
        self.tester.post('/api/v1/menu/3',
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/menu/2',
                         headers =dict(access_token = result['token']))
        
        self.tester.post('/api/v1/orders/3',
                                  headers =dict(access_token = result['token']))
        #orders 
        self.tester.post('/api/v1/orders/2',
                                  headers =dict(access_token = result['token']))
        
        responsev=self.tester.delete('/api/v1/orders/2',
                                  headers =dict(access_token = result['token']))

        self.assertIn(u"Successfully deleted", responsev.data)

    def test_fail_delete_orders(self):
        """tests that an order can be deleted"""
        result=login(self.tester)
        add_meal(self.tester,result)
        #add meals to menu
        self.tester.post('/api/v1/menu/3',
                         headers =dict(access_token = result['token']))
        self.tester.post('/api/v1/menu/2',
                         headers =dict(access_token = result['token']))
        
        self.tester.post('/api/v1/orders/3',
                                  headers =dict(access_token = result['token']))
        #orders 
        self.tester.post('/api/v1/orders/2',
                                  headers =dict(access_token = result['token']))
        
        responsev=self.tester.delete('/api/v1/orders/5',
                                  headers =dict(access_token = result['token']))

        self.assertIn(u"Order does not exist", responsev.data)
        


if __name__=="__main__":
    unittest.main()#pragma:no cover
