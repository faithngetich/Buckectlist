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
    # executed prior to each each test
    def setUp(self):
        app = create_app('test')
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()


        # mail.init_app(app)
        self.assertEquals(app.debug, True)

    # executed after each test
    def tearDown(self):
        pass

    def test_add_user(self):
        with self.app.app_context():
            db.session.add(User(name='testr', email='test@mail.com'))
            db.session.commit()
    
    def test_encode_auth_token(self):
        user = User(
            username='testm',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

#     def test_decode_auth_token(self):
#         user = User(username='testm',password='test')
#         db.session.add(user)
#         db.session.commit()
#         auth_token = user.encode_auth_token(user.id)
#         self.assertTrue(isinstance(auth_token, bytes))
#         self.assertTrue(User.decode_auth_token(auth_token) == 1)

#     def test_registration(self):
#         """ Test for user registration """
#         with self.client:
#             response = self.client.post(
#                 '/auth/register',
#                 data=json.dumps(dict(
#                     username='jom',
#                     password='123456'
#                 )),
#                 content_type='application/json'
#             )
#             data = json.loads(response.data.decode())
#             self.assertTrue(data['status'] == 'success')
#             self.assertTrue(data['message'] == 'Successfully registered.')
#             self.assertTrue(data['auth_token'])
#             self.assertTrue(response.content_type == 'application/json')
#             self.assertEqual(response.status_code, 201)

#     def test_registered_user_login(self):
#         """ Test for login of registered-user login """
#         with self.client:
#             # user registration
#             resp_register = self.client.post(
#                 '/users',
#                 data=json.dumps(dict(
#                     username='jom',
#                     password='123456'
#                 )),
#                 content_type='application/json',
#             )
#             data_register = json.loads(resp_register.data.decode())
#             self.assertTrue(data_register['status'] == 'success')
#             self.assertTrue(
#                 data_register['message'] == 'Successfully registered.'
#             )
#             self.assertTrue(data_register['auth_token'])
#             self.assertTrue(resp_register.content_type == 'application/json')
#             self.assertEqual(resp_register.status_code, 201)
#             # registered user login
#             response = self.client.post(
#                 '/auth/login',
#                 data=json.dumps(dict(
#                     username='jom',
#                     password='123456'
#                 )),
#                 content_type='application/json'
#             )
#             data = json.loads(response.data.decode())
#             self.assertTrue(data['status'] == 'success')
#             self.assertTrue(data['message'] == 'Successfully logged in.')
#             self.assertTrue(data['auth_token'])
#             self.assertTrue(response.content_type == 'application/json')
#             self.assertEqual(response.status_code, 200)

#     def test_registered_with_already_registered_user(self):
#         """ Test registration with already registered email"""
#         user = User(
#             username='jom',
#             password='test'
#         )
#         db.session.add(user)
#         db.session.commit()
#         with self.client:
#             response = self.client.post(
#                 '/users',
#                 data=json.dumps(dict(
#                     username='jom',
#                     password='123456'
#                 )),
#                 content_type='application/json'
#             )
#             data = json.loads(response.data.decode())
#             self.assertTrue(data['status'] == 'fail')
#             self.assertTrue(
#                 data['message'] == 'User already exists. Please Log in.')
#             self.assertTrue(response.content_type == 'application/json')
#             self.assertEqual(response.status_code, 202)

    
#     # # helper methods
#     # def register(self, email, password):
#     #     return self.app.post(
#     #         '/register',
#     #         data=dict(email=email, password=password),
#     #         follow_redirects=True
#     #     )

#     # def login(self, email, password):
#     #     return self.app.post(
#     #         '/login',
#     #         data=dict(email=email, password=password),
#     #         follow_redirects=True
#     #     )

#     # # tests
#     # # def test_registration(self):
#     # #     """ Test for user registration """
#     # #     with self.client:
#     # #         response = self.client.post(
#     # #             '/auth/register',
#     # #             data=json.dumps(dict(
#     # #                 username='faihuna',
#     # #                 password='123456'
#     # #             )),
#     # #             content_type='application/json'
#     # #         )
#     # #     data = json.loads(response.data.decode())
#     # #     self.assertTrue(data['status'] == 'success')
#     # #     self.assertTrue(data['message'] == 'Successfully registered.')
#     # #     self.assertTrue(data['auth_token'])
#     # #     self.assertTrue(response.content_type == 'application/json')
#     # #     self.assertEqual(response.status_code, 201)
#     # def test_valid_user_registration(self):
#     #     """Test user provide required details for registration"""
#     #     self.app.get('/users/login', follow_redirects=True)
#     #     response = self.register('faithngetich188@gmail.com', '123')
#     #     self.assertIn(response.status_code, 201)

#     # def test_duplicate_email_user_registration_error(self):
#     #     """Test user does not register twice"""
#     #     self.app.get('/register', follow_redirects=True)
#     #     self.register('faithngetich188@gmail.com', '123')
#     #     self.app.get('/register', follow_redirects=True)
#     #     response = self.register('faithngetich188@gmail.com', '123')
#     #     self.assertIn('ERROR! Email (faithngetich188@gmail.com) already exists.', response.data)

#     # def test_missing_field_user_registration_error(self):
#     #     """Test user provide all required details"""
#     #     self.app.get('/register', follow_redirects=True)
#     #     response = self.register('faithngetich188@gmail.com','')
#     #     self.assertIn('This field is required.', response.data)
    
#     # def test_valid_login(self):
#     #     self.app.get('/register', follow_redirects=True)
#     #     self.register('faithngetich188@gmail.com', '123')
#     #     self.app.get('/logout', follow_redirects=True)
#     #     self.app.get('/login', follow_redirects=True)
#     #     response = self.login('faithngetich188@gmail.com', '123')
#     #     self.assertIn('faithngetich188@gmail.com', response.data)

#     # def test_login_without_registering(self):
#     #     """Test user registers for the firm time"""
#     #     self.app.get('/login', follow_redirects=True)
#     #     response = self.login('faithngetich188@gmail.com', '123')
#     #     self.assertIn('ERROR! Incorrect login credentials.', response.data)

#     # def test_valid_logout(self):
#     #     self.app.get('/register', follow_redirects=True)
#     #     self.register('faithngetich188@gmail.com', '123')
#     #     self.app.get('/login', follow_redirects=True)
#     #     self.login('faithngetich188@gmail.com', '123')
#     #     response = self.app.get('/logout', follow_redirects=True)
#     #     self.assertIn('Goodbye!', response.data)
    
#     # def test_change_email_address(self):
#     #     self.app.get('/register', follow_redirects=True)
#     #     self.register('faithngetich188@gmail.com', '123')
#     #     self.app.post('/email_change', data=dict(email='faithngetich188@gmail.com'), follow_redirects=True)
#     #     response = self.app.get('/user_profile')
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIn('Email Address', response.data)
#     #     self.assertIn('faithngetich188@yahoo.com', response.data)
#     #     self.assertNotIn('faithngetich188@gmail.com', response.data)

#     # def test_change_email_address_with_existing_email(self):
#     #     self.app.get('/register', follow_redirects=True)
#     #     self.register('faithngetich188@gmail.com', '123')
#     #     response = self.app.post('/email_change', data=dict(email='faithngetich188@gmail.com'), follow_redirects=True)
#     #     self.assertEqual(response.status_code, 400)
#     #     self.assertIn('Sorry, that email already exists!', response.data)
#     #     self.assertIn('Current Email: faithngetich188@gmail.com', response.data)
#     #     self.assertIn('Please enter your new email address:', response.data)

# if __name__ == "__main__":
#     unittest.main()
