import unittest
import json
from app import APP

class TestUserApi(unittest.TestCase):
    def setUp(self):
        self.tester = APP.test_client(self)
        
    def test_successful_signup(self):
        """Test that a user can be signed in"""
        
        response = self.tester.post('/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail.com',
                                                        password='lantern')))
        self.assertIn(u"Successfully signed up",response.data)
        self.assertEqual(response.status_code, 200)

if __name__=="__main__":
    unittest.main()
