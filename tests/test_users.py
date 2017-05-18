import os
import unittest
from app import create_app
from app.config import config_by_name 
from app import db

TEST_DB = 'user.db'

class UsersTests(unittest.TestCase):
    """setup and teardown"""
    # def create_app(self):
    #     app = create_app('test')
    #     return app
    # executed prior to each each test
    def setUp(self):
        app = create_app('test')
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()


        # mail.init_app(app)
        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    # helper methods
    def register(self, email, password):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    # tests
    def test_valid_user_registration(self):
        """Test user provide required details for registration"""
        self.app.get('/register', follow_redirects=True)
        response = self.register('faithngetich188@gmail.com', '123')
        self.assertIn('Thanks for registering!', response.data)

    def test_duplicate_email_user_registration_error(self):
        """Test user does not register twice"""
        self.app.get('/register', follow_redirects=True)
        self.register('faithngetich188@gmail.com', '123')
        self.app.get('/register', follow_redirects=True)
        response = self.register('faithngetich188@gmail.com', '123')
        self.assertIn('ERROR! Email (faithngetich188@gmail.com) already exists.', response.data)

    def test_missing_field_user_registration_error(self):
        """Test user provide all required details"""
        self.app.get('/register', follow_redirects=True)
        response = self.register('faithngetich188@gmail.com', '123', '')
        self.assertIn('This field is required.', response.data)
    
    def test_valid_login(self):
        self.app.get('/register', follow_redirects=True)
        self.register('faithngetich188@gmail.com', '123')
        self.app.get('/logout', follow_redirects=True)
        self.app.get('/login', follow_redirects=True)
        response = self.login('faithngetich188@gmail.com', '123')
        self.assertIn('faithngetich188@gmail.com', response.data)

    def test_login_without_registering(self):
        """Test user registers for the firm time"""
        self.app.get('/login', follow_redirects=True)
        response = self.login('faithngetich188@gmail.com', '123')
        self.assertIn('ERROR! Incorrect login credentials.', response.data)

    def test_valid_logout(self):
        self.app.get('/register', follow_redirects=True)
        self.register('faithngetich188@gmail.com', '123')
        self.app.get('/login', follow_redirects=True)
        self.login('faithngetich188@gmail.com', '123')
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn('Goodbye!', response.data)
    
    def test_change_email_address(self):
        self.app.get('/register', follow_redirects=True)
        self.register('faithngetich188@gmail.com', '123')
        self.app.post('/email_change', data=dict(email='faithngetich188@gmail.com'), follow_redirects=True)
        response = self.app.get('/user_profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Email Address', response.data)
        self.assertIn('faithngetich188@yahoo.com', response.data)
        self.assertNotIn('faithngetich188@gmail.com', response.data)

    def test_change_email_address_with_existing_email(self):
        self.app.get('/register', follow_redirects=True)
        self.register('faithngetich188@gmail.com', '123')
        response = self.app.post('/email_change', data=dict(email='faithngetich188@gmail.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sorry, that email already exists!', response.data)
        self.assertIn('Current Email: faithngetich188@gmail.com', response.data)
        self.assertIn('Please enter your new email address:', response.data)

if __name__ == "__main__":
    unittest.main()
