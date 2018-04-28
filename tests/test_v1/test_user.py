import unittest
import json
from app import APP

class TestUserApi(unittest.TestCase):
    def setUp(self):
        self.tester = APP.test_client(self)
        
    def test_successful_signup(self):
        """Test that a user can be signed in"""
        
        response = self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail.com',
                                                        password='lantern')))
        self.assertIn(u"Successfully signed up",response.data)
        self.assertEqual(response.status_code, 201)

    def test_unique_user_signup(self):
        """Test that a unque user can be added"""
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        response = self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        self.assertIn(u"User already exists",response.data)
        self.assertEqual(response.status_code, 401)

    def test_wrong_format_credentials_signup(self):
        """Test that a user cannot be added with wrong email format"""
        
        response = self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='you@@gmail.com',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'''Repetition of "@" is not allowed''')
        self.assertEqual(response.status_code, 422)

    def test_wrong_email_end_signup(self):
        """Test that a user cannot be added with wrong email format"""
        
        response = self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'Input a valid email')
        self.assertEqual(response.status_code, 422)

    def test_string_type_email_signup(self):
        """Test that a user cannot be added with wrong email format"""
        
        response = self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='yougmail.com',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'"@" is missing')
        self.assertEqual(response.status_code, 422)

    def test_correct_credential_login(self):
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        result = json.loads(login.data.decode())
        self.assertIn(u'token',result)
        self.assertEqual(login.status_code, 200)

    def test_incorrect_credential_login(self):
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='wrongone')))
        result = json.loads(login.data.decode())
        self.assertIn(u'Authorize with correct password',result['message'])
        self.assertEqual(login.status_code, 401)

    def test_incorrect_user_login(self):
        login = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='mene@gmail.com',
                                                        password='wrongone')))
        result = json.loads(login.data.decode())
        self.assertIn(u"User does not exist",result['message'])
        self.assertEqual(login.status_code, 404)

    def test_wrong_format_credentials_login(self):
        """Test that a user cannot login with wrong email format"""
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        
        response = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='me@@gmail.com',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'''Repetition of "@" is not allowed''')
        self.assertEqual(response.status_code, 401)

    def test_wrong_email_end_login(self):
        """Test that a user cannot login with wrong email format"""
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail.com',
                                                        password='lantern')))
        
        response = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Input a valid email")
        self.assertEqual(response.status_code, 401)

    def test_email_missing_character_login(self):
        """Test that a user cannot login with email missing '@'"""
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        
        response = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='mgmail.com',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'"@" is missing')
        self.assertEqual(response.status_code, 401)

    def test_non_string_email_type_login(self):
        """Test that a user cannot login with wrong email format"""
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        
        response = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email=1234,
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Input should be a string")
        self.assertEqual(response.status_code, 401)

    def test_empty_email_login(self):
        """Test that a user cannot login with wrong email format"""
        self.tester.post('api/v1/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        
        response = self.tester.post('api/v1/auth/login',content_type='application/json',
                                   data =json.dumps( {}))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Authorize with email and password")
        self.assertEqual(response.status_code, 401)
    

if __name__=="__main__":
    unittest.main()#pragma:no cover
