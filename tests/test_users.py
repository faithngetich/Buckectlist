import os
import json
import unittest
from app import create_app
from app.config import config_by_name 
from app.models.models import User, BucketList, Item
from app.models import db

TEST_DB = 'test.db'

class UsersTests(unittest.TestCase):
    """setup and teardown"""
    def setUp(self):
        self.app = create_app('test')
        # simulates the get/post environment
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_user(self):
        # binds the app with the current context
        with self.app.app_context():
            db.session.add(User(username='testr', password='test'))
            db.session.commit()
    
    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='jom',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] ==  'User created successfully')
            self.assertEqual(response.status_code, 201)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user register
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='jom',
                    password='123456'
                )),
                content_type='application/json'
            )
            # user login
            resp_register = self.client.post(
                '/api/login',
                data=json.dumps(dict(
                    username='jom',
                    password='123456'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register["access_token"])
            self.assertEqual(resp_register.status_code, 200)
    
    def test_registered_user_wrong_login(self):
        """ Test for login of registered-user login with bad credentials """
        with self.client:
            # user register
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='jom',
                    password='123456'
                )),
                content_type='application/json'
            )
            # user login
            resp_register = self.client.post(
                '/api/login',
                data=json.dumps(dict(
                    username='jom',
                    password='1256'
                )),
                content_type='application/json',
            )
            data = json.loads(resp_register.data.decode())
            self.assertTrue(data['description'] == "Invalid credentials")
            self.assertTrue(data['error'] == 'Bad Request')
            self.assertEqual(resp_register.status_code, 401)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = User(
            username='jom',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
               '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='jom',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['Error'] == 'Duplicate Username')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertEqual(response.status_code, 409) 


    def test_missing_field_user_registration_error(self):
        """Test user provide all required details"""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400) 
            self.assertTrue(data['message']["username"] ==  'Username Required')
        
   
        
if __name__ == "__main__":
    unittest.main()
