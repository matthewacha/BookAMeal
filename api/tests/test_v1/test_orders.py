import unittest
import json
from api import APP, DB

def login(tester):
    tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail.com',
                                                        password='lantern')))
    login = tester.post('api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail.com',
                                                        password='lantern')))
    result = json.loads(login.data.decode())
    return result

def add_meal(tester, result):
    tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
    response = tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
    result2 = json.loads(response.data.decode())
    tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))
    tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)),
                         headers =dict(K_access_token = result2['token']))
    response=tester.post('/api/v2/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Chicken',
                                                        price=15000)),
                         headers =dict(K_access_token = result2['token']))
    stuff = {"response":response,"result2":result2}
    return stuff

class TestOrders(unittest.TestCase):
    def setUp(self):
        self.tester = APP.test_client(self)
        DB.create_all()
        DB.session.commit()
    def tearDown(self):
        DB.drop_all()
        
    def test_make_order(self):
        """test that a customer can make an order"""
        result=login(self.tester)
        stuff = add_meal(self.tester,result)
        result2 = stuff["result2"]
        
        """post to day's menu"""
        self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/menus/1',content_type='application/json',
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))

        #make an order
        self.tester.post('/api/v2/orders/Special/1',
                                  headers =dict(access_token = result['token']))
        response=self.tester.post('/api/v2/orders/Special/2',
                                  headers =dict(access_token = result['token']))
        self.assertIn(u"Order sent", response.data)

    def test_fail_make_order(self):
        """test that a customer cannot make an order"""
        result=login(self.tester)
        stuff = add_meal(self.tester,result)
        result2 = stuff["result2"]
        
        """post to day's menu"""
        self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/menus/1',content_type='application/json',
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))

        #make an order
        self.tester.post('/api/v2/orders/Special/1',
                                  headers =dict(access_token = result['token']))
        response=self.tester.post('/api/v2/orders/Special/5',
                                  headers =dict(access_token = result['token']))
        self.assertIn(u"Meal does not exist", response.data)

        response=self.tester.post('/api/v2/orders/Chillax/2',
                                  headers =dict(access_token = result['token']))
        self.assertIn(u"Menu does not exist", response.data)

        response=self.tester.post('/api/v2/orders/Special/3',
                                  headers =dict(access_token = result['token']))
        self.assertIn(u"Meal does not exist in menu", response.data)

        response=self.tester.post('/api/v2/orders/Special/3',
                                  headers =dict(access_token = u'12435142r'))
        self.assertIn(u"Unauthorized access, please login", response.data)

        response=self.tester.post('/api/v2/orders/Special/3',
                                  headers =dict(S_access_token = u'12435142r'))
        self.assertIn(u"Token is missing", response.data)

    def test_get_all_orders(self):
        """test that a customer can get all orders from menu"""
        result=login(self.tester)
        stuff = add_meal(self.tester,result)
        result2 = stuff["result2"]
        
        #post to day's menu
        self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/menus/1',content_type='application/json',
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))

        #make an order
        self.tester.post('/api/v2/orders/Special/1',
                                  headers =dict(access_token = result['token']))
        self.tester.post('/api/v2/orders/Special/1',
                                  headers =dict(access_token = result['token']))
        
        response=self.tester.get('/api/v2/orders/Special',
                                  headers =dict(access_token = result['token']))
        rv = json.loads(response.data.decode())

        self.assertEqual(len(rv['Orders']), 2)

        

    def test_delete_orders(self):
        """tests that an order can be deleted"""
        result=login(self.tester)
        stuff = add_meal(self.tester,result)
        result2 = stuff["result2"]
        
        #post to day's menu
        self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/menus/1',content_type='application/json',
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))

        #make an order
        self.tester.post('/api/v2/orders/Special/1',
                                  headers =dict(access_token = result['token']))
        self.tester.post('/api/v2/orders/Special/1',
                                  headers =dict(access_token = result['token']))
        self.tester.post('/api/v2/orders/Special/2',
                                  headers =dict(access_token = result['token']))
        
        response=self.tester.delete('/api/v2/orders/2',
                                  headers =dict(access_token = result['token']))

        self.assertIn(u"Successfully deleted", response.data)

    def test_fail_delete_orders(self):
        """tests that an order can be deleted"""
        result=login(self.tester)
        stuff = add_meal(self.tester,result)
        result2 = stuff["result2"]
        
        #post to day's menu
        self.tester.post('/api/v2/menus/2',content_type='application/json',
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/menus/1',content_type='application/json',
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))

        #make an order
        self.tester.post('/api/v2/orders/Special/1',
                                  headers =dict(access_token = result['token']))
        self.tester.post('/api/v2/orders/Special/1',
                                  headers =dict(access_token = result['token']))
        self.tester.post('/api/v2/orders/Special/2',
                                  headers =dict(access_token = result['token']))
        
        response=self.tester.delete('/api/v2/orders/5',
                                  headers =dict(access_token = result['token']))

        self.assertIn(u"Order does not exist", response.data)

    def test_adminGetOrder(self):
        """test that a meal can be deleted from a menu"""
        result=login(self.tester)
        stuff = add_meal(self.tester,result)
        result2 = stuff["result2"]
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
        data = json.dumps(dict(menuName='Special')),
                         headers =dict(K_access_token = result2['token']))
        self.tester.post('/api/v2/menus/3',content_type='application/json',
        data = json.dumps(dict(menuName='Special')), headers =dict(K_access_token = result2['token']))

        rv = self.tester.get('/api/v2/orders/admin', headers =dict(K_access_token = result2['token']))
        rvs = json.loads(rv.data.decode())
        self.assertIn(u"You have no orders to serve", rvs['message'])
        self.assertEqual(response.status_code, 200)

        self.tester.post('/api/v2/orders/Special/3',
                                  headers =dict(access_token = result['token']))
        self.tester.post('/api/v2/orders/Special/2',
                                  headers =dict(access_token = result['token']))
        self.tester.post('/api/v2/orders/Special/2',
                                  headers =dict(access_token = result['token']))
        
        rv = self.tester.get('/api/v2/orders/admin', headers =dict(K_access_token = result2['token']))
        rvs = json.loads(rv.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(3, len(rvs['Orders']))
        
        


if __name__=="__main__":
    unittest.main()#pragma:no cover
