import unittest
import json
from app import APP

class TestUserApi(unittest.TestCase):
    def setUp(self):
        self.tester = APP.test_client(self)
        
    def test_make_order(self):
        """test that a customer can make an order"""
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Chicken',
                                                        price=15000)))
        """post to day's menu"""
        self.tester.post('/api/v1/menu/1')
        self.tester.post('/api/v1/menu/2')

        """make an order"""
        response=self.tester.post('/api/v1/orders/2')
        self.assertIn(u"Successfully sent", response.data)

    def test_get_all_orders(self):
        """test that a customer can get all orders from menu"""
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Chicken',
                                                        price=15000)))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=55000)))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fish',
                                                        price=5000)))
        self.tester.post('/api/v1/menu/1')
        self.tester.post('/api/v1/menu/2')
        self.tester.post('/api/v1/orders/2')

        response=self.tester.get('/api/v1/orders')
        self.assertIn(u"Chicken", response.data)
        
        

if __name__=="__main__":
    unittest.main()
