import unittest
import json
from api import APP, DB

class TestUserApi(unittest.TestCase):
    def setUp(self):
        """run at the start of every test case"""
        self.tester = APP.test_client(self)
        DB.create_all()
        DB.session.commit()
    def tearDown(self):
        """run at the end of every test case"""
        DB.drop_all()
        
    def test_successful_signup(self):
        """Test that a user can be signed in"""
        
        response = self.tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail.com',
                                                        password='lantern')))
        self.assertIn(u"Successfully signed up",response.data)
        self.assertEqual(response.status_code, 201)

    def test_unique_user_signup(self):
        """Test that a unque user can be added"""
        self.tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        response = self.tester.post('api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        self.assertIn(u"User already exists",response.data)
        self.assertEqual(response.status_code, 401)

    def test_wrong_format_credentials_signup(self):
        """Test that a user cannot be added with wrong email format"""
        
        response = self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='you@@gmail.com',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'''Repetition of "@" is not allowed''')
        self.assertEqual(response.status_code, 401)

    def test_wrong_email_end_signup(self):
        """Test that a user cannot be added with wrong email format"""
        
        response = self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'Input a valid email')
        self.assertEqual(response.status_code, 401)

    def test_string_type_email_signup(self):
        """Test that a user cannot be added with wrong email format"""
        
        response = self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='yougmail.com',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'"@" is missing')
        self.assertEqual(response.status_code, 401)

    def test_correct_token_generated_login(self):
        """tests that token is generated on login"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        result = json.loads(login.data.decode())
        self.assertIn(u'token',result)
        self.assertEqual(login.status_code, 200)

    def test_incorrect_password_login(self):
        """test user can not login with incorrect password"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='wrongone')))
        result = json.loads(login.data.decode())
        self.assertIn(u'Authorize with correct password',result['message'])
        self.assertEqual(login.status_code, 401)

    def test_incorrect_user_login(self):
        """test that non existent user can not login"""
        login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='mene@gmail.com',
                                                        password='wrongone')))
        result = json.loads(login.data.decode())
        self.assertIn(u"User does not exist",result['message'])
        self.assertEqual(login.status_code, 404)

    def test_wrong_format_credentials_login(self):
        """Test that a user cannot login with wrong email format"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        
        response = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='me@@gmail.com',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'''Repetition of "@" is not allowed''')
        self.assertEqual(response.status_code, 401)

    def test_wrong_email_end_login(self):
        """Test that a user cannot login with wrong email format"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail.com',
                                                        password='lantern')))
        
        response = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Input a valid email")
        self.assertEqual(response.status_code, 401)

    def test_email_missing_character_login(self):
        """Test that a user cannot login with email missing '@'"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        
        response = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='mgmail.com',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'"@" is missing')
        self.assertEqual(response.status_code, 401)

    def test_non_string_email_type_login(self):
        """Test that a user cannot login with wrong email format"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        
        response = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email=1234,
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Please input a string")
        self.assertEqual(response.status_code, 401)

    def test_no_email_login(self):
        """Test that a user cannot login with no credentials"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))
        
        response = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( {}))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Authorize with email and password")
        self.assertEqual(response.status_code, 401)

    def test_empty_email_login(self):
        """Test that a user cannot login with wrong email format"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='lantern')))

        response = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='   ',
                                                        password='asm')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"You cannot send an empty string")
        self.assertEqual(response.status_code, 401)

    def test_empty_password_login(self):
        """Test that a user cannot login with no password"""

        response = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='a@f.com',
                                                        password='  ')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"You cannot send an empty string")
        self.assertEqual(response.status_code, 401)

    def test_empty_email_login(self):
        """Test that a user cannot login with empty email"""

        response = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='',
                                                        password='lantern')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Authorize with email and password")
        self.assertEqual(response.status_code, 401)

    def test_no_password_login(self):
        """Test that a user cannot login with no  password"""

        response = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( {"email":"a@d.com", "password":""}))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Authorize with email and password")
        self.assertEqual(response.status_code, 401)

    def test_long_email_login(self):
        """Test that a user cannot login with wrong email format"""

        response = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( {"email":"aaaaaaaaaaassssssssssssssssssddddddddddddddddddddddddddddddddddddddddddddddddddddddddd@ffffffffffffffffffffffffffffffffffffffffffffff.com", "password":"animal"}))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Email should be less than 60 characters")
        self.assertEqual(response.status_code, 401)
    
    def test_admin_signup(self):
        """tests that a logged in user can set admin to True"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail.com',
                                                        password='lantern')))
        result = json.loads(login.data.decode())
        response = self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())
        self.assertEqual(result2['message'], u"User set to admin")
        self.assertEqual(response.status_code, 201)

    def test_admin_already_set(self):
        """tests that a logged in user can set admin to True"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='men@gmail.com',
                                                        password='lantern')))
        result = json.loads(login.data.decode())
        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())
        self.assertEqual(result2['message'], u"User is already admin")
        self.assertEqual(response.status_code, 401)

    def test_login_as_admin(self):
        """tests that a logged in user can login as admin"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='seme@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='seme@gmail.com',
                                                        password='lantern')))
        result = json.loads(login.data.decode())

        self.tester.post('/api/v2/auth/Admin',headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())
        self.assertTrue(result2['token'])
        self.assertEqual(response.status_code, 200)

    def test_fail_login_as_admin(self):
        """tests that a logged in user can login as admin"""
        self.tester.post('/api/v2/auth/signup',content_type='application/json',
                                   data =json.dumps( dict(email='seme@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                                   data =json.dumps( dict(email='seme@gmail.com',
                                                        password='lantern')))
        result = json.loads(login.data.decode())

        response = self.tester.post('/api/v2/auth/adminLogin', headers =dict(access_token = result['token']))
        result2 = json.loads(response.data.decode())
        self.assertEqual(result2["message"], u"Sorry, you are not authorized")
        self.assertEqual(response.status_code, 401)

if __name__=="__main__":
    unittest.main()#pragma:no cover
