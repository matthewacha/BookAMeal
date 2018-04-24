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
        self.assertEqual(response.status_code, 201)

    def test_unique_user_signup(self):
        """Test that a unque user can be added"""
        self.tester.post('/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        response = self.tester.post('/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        self.assertIn(u"User already exists",response.data)
        self.assertEqual(response.status_code, 401)

    def test_wrong_format_credentials_signup(self):
        """Test that a user cannot be added with wrong email format"""
        
        response = self.tester.post('/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='you@@gmail.com',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'''Repetition of "@" is not allowed''')
        self.assertEqual(response.status_code, 422)

    def test_correct_credential_login(self):
        self.tester.post('/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        result = json.loads(login.data.decode())
        self.assertIn(u'token',result)
        self.assertEqual(login.status_code, 200)

    

if __name__=="__main__":
    unittest.main()
