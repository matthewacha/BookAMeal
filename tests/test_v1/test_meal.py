import unittest
import json
from app import APP

class TestUserApi(unittest.TestCase):
    def setUp(self):
        self.tester = APP.test_client(self)

    def test_create_meal(self):
        """test that a meal option can be succesfully added"""
        response= self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)))
        result=json.loads(response.data.decode())
        self.assertIn(u'Successfully added meal option', result['message'])
        self.assertEqual(response.status_code, 201)

    def test_fail_create_meal(self):
        """test that a meal option cannot be added if strin price
        is passed instead of integer"""
        response= self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price='anim45')))
        result=json.loads(response.data.decode())
        self.assertIn(u'Meal option already exists, try another', result['message'])
        self.assertEqual(response.status_code, 401)

    def test_get_all_meals(self):
        """test that all meal options can be retrieved"""
        self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)))
        self.tester.post('api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)))
        response=self.tester.get('api/v1/meals/')
        result=json.loads(response.data.decode())

        self.assertEqual(len(result['meals']), 2)

    def test_update_meal(self):
        """test that a meal option can be updated"""
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)))
        response=self.tester.put('/api/v1/meals/2',content_type='application/json',
                                  data=json.dumps(dict(name='Beans n fries',
                                                       price=3500)))
        self.assertIn(u'Successfully updated meal', response.data)
        self.assertEqual(response.status_code, 201)

    def test_fail_update_meal(self):
        """test that a non existent meal option cannot be updated """
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)))
        response=self.tester.put('/api/v1/meals/3',content_type='application/json',
                                  data=json.dumps(dict(name='Beans fries',
                                                       price=4500)))
        self.assertIn(u'Meal option does not exist', response.data)
        self.assertEqual(response.status_code, 404)

    def test_delete_meal(self):
        """test that a meal can be deleted """
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)))
        response=self.tester.delete('/api/v1/meals/2')
       
        self.assertIn(u'Successfully deleted meal', response.data)
        self.assertEqual(response.status_code, 200)

    def test_fail_to_delete_meal(self):
        """test that a non existent meal option cannot be deleted """
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Fries',
                                                        price=5000)))
        self.tester.post('/api/v1/meals/', content_type='application/json',
                                   data =json.dumps( dict(name='Beans',
                                                        price=5000)))
        response=self.tester.delete('/api/v1/meals/3')
        self.assertIn(u'Failed to delete meal', response.data)
        self.assertEqual(response.status_code, 401)
    
        

if __name__=='__main__':
    unittest.main()
