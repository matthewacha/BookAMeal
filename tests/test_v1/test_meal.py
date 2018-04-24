import unittest
import json
from app import APP

class TestUserApi(unittest.TestCase):
    def setUp(self):
        self.tester = APP.test_client(self)

    def test_create_meal(self):
        """test that a meal option can be succesfully added"""
        response= self.tester.post('meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)))
        result=json.loads(response.data.decode())
        self.assertIn(u'Successfully added meal option', result['message'])
        self.assertEqual(response.status_code, 201)

    def test_fail_create_meal(self):
        """test that a meal option cannot be added if strin price
        is passed instead of integer"""
        response= self.tester.post('meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price='anim45')))
        result=json.loads(response.data.decode())
        self.assertIn(u'Meal option already exists, try another', result['message'])
        self.assertEqual(response.status_code, 401)

    def test_get_all_meals(self):
        """test that all meal options can be retrieved"""
        self.tester.post('meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)))
        self.tester.post('meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)))
        response=self.tester.get('meals/')
        result=json.loads(response.data.decode())
        
        self.assertEqual(len(result['meals']), 2)

    def test_update_meal(self):
        """test that a meal option can be updated"""
        self.tester.post('meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)))
        self.tester.post('meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)))
        response=self.tester.put('meals/2',content_type='appliation/json',
                                  data=json.dumps(dict(name='Beans fries',
                                                       price=4500)))
        #result=json.loads(response.data.decode())
        self.assertIn(u'Successfully updated meal', response.data)
        self.assertEqual(response.status_code, 201)
        

if __name__=='__main__':
    unittest.main()
