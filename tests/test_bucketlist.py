import os
import json
import unittest 
from flask_testing import TestCase
from app.models import db
from app import create_app
from app.config import Config
from app.models.models import User, BucketList, Item


# class BucketListTestCases(unittest.TestCase):
    # def setUp(self):
    #     """"Initialize the app and set up test variables."""
    #     # simulates the get/post environments
    #     self.app = create_app(config_name="test")
    #     self.client = self.app.test_client
    #     self.bucketlist = {'name': 'Travels'}
    #     self.user_details = json.dumps({"username":"Tester", "password1":"Function"})
    #     self.client().post('/api/v1/users/login', data=self.user_details)
    #     self.user_login = json.dumps({"username":"Tester","password":"Function"})
    #     login = self.client().post('/api/v1/users', data = self.user_login)
    #     json_login = json.loads(login.data)
    #     # self.token = json_login['auth_token']
    #     # binds the app with the current context
    #     with self.app.app_context():
    #         db.create_all()

    # def test_homepage_route(self):
    #     """Test the route /api/v1/"""
    
    #     request = self.client().get('/')
    #     self.assertEqual(request.status_code, 200)
    
class TestDevelopmentConfig(unittest.TestCase):
    def create_app(self):
        app.config.from_object('project.server.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite://sqlite:@localhost/flask_jwt_auth')


    def setUp(self):
        app = create_app('test')
        self.user_details = json.dumps({"username":"Tester", "password1":"Function","password2":"Function"})
        # simulates the get/post environments
        self.app = app.test_client()
        # binds the app with the current context
        with app.app_context():
            db.create_all()

        # mail.init_app(app)
        self.assertEquals(app.debug, False)

    

    # def test_login(self):
        # """Tests that a user can be logged into the app and a token generated."""
        # response = self.client().post('/api/users', data=self.user_login    )
        # self.assertEqual(response.status_code, 200)
        # json_dict = json.loads(response.data)
        # self.assertIn(json_dict['User']['username'], "Tester")
    

#     # helper methods
#     def login(self):
#         response = self.client.post('/users/login',
#                                     data=json.dumps(
#                                         {"username": "com",
#                                          "password": "password"}),
#                                     content_type='application/json'
#                                     )

#         data = json.loads(response.get_data(as_text=True))
#         return data["access_token"]

#     def get_auth_header(self):
#         token = self.login()
#         return {'Authorization': 'JWT %s' % token,
#                 'Content-type': 'application/json'
#                 }

#     # executed after each test
#     def tearDown(self):
#         models.User.query.delete()
#         models.BucketList.query.delete()
#         models.ListItem.query.delete()

#         user = models.User(
#             username="mcom",
#             password="password"
#         )

#         db.session.add_all([user])
#         db.session.commit()

#     def create_bucketlist(self):
#         headers = self.get_auth_header()
#         bucketlist = {
#             "name": "BucketList1",
#         }
#         self.client.post('/bucketlists',
#                          data=json.dumps(bucketlist),
#                          headers=headers
#                          )

#     def register_2nd_user(self):
#         '''Registers other user for testing'''
#         user_data = {
#             "username": "fcom",
#             "password": "password",
#         }

#         response = self.client.post(
#             "/auth/register",
#             content_type="application/json",
#             data=json.dumps(user_data)
#         )
#         return response

#     def add_bucketlist_item(self):
#         '''adds a bucketlist item'''
#         headers = self.get_auth_header()

#         item = {"name": "Foo the bar"}
#         self.client.post("/bucketlists/<int:bucketlist_id>/items",
#                          data=json.dumps(item),
#                          headers=headers
#                          )
    
#     def add_test_user(self):
#         user_data = {
#             "username": "mcom",
#             "password": "password",
#         }

#         self.client.post(
#             "/users/login",
#             content_type="application/json",
#             data=json.dumps(user_data)
#         )
# class TestAuthentication(BaseTestCase):
#     def test_create_bucketlist(self):
#         headers = self.get_auth_header()
#         bucketlist = {
#             "name": "BucketList1",
#         }
#         response = self.client.post('/bucketlists',
#                                     data=json.dumps(bucketlist),
#                                     headers=headers
#                                     )
#         assert response.status_code == 201


    # def register(self, username, email, password):
    #     return self.app.post('/users/login', data=dict(username=username, email=email, password=password),follow_redirects=True)
    
    # def login(self, email, password):
    #     data = dict(email=email, password=password, follow_redirects=True)
    #     return self.app.post('/login', data)

    # def register_user(self):
    #     self.app.get('/register', follow_redirects=True)
    #     self.register('faithngetich188@gmail.com', '123')

    # def logout_user(self):
    #     return self.app.post('/logout', follow_redirects=True)

    # def add_buckectlist(self):
    #     self.register_user()
    #     user1 = User.query.filter_by(email='faithngetich188@gmail.com').first()
    #     bucketlist1 = Bucketlist('Travel to bermuda',user1.user_id, True)
    #     bucketlist2 = Bucketlist('Get my name to the Guinness Book of Record',user1.id, True)
    #     bucketlist3 = Bucketlist('Travel to Delhi',user1.id, False)
    #     bucketlist4 = Bucketlist('climb ',user1.id, False)
    #     bucketlist5 = Bucketlist('Travel to bermuda',user1.id, False)
    #     db.session.add(bucketlist1)
    #     db.session.add(bucketlist2)
    #     db.session.add(bucketlist3)
    #     db.session.add(bucketlist4)
    #     db.session.commit

    # Tests
    # def test_valid_user_registration(self):
    #     response = self.register('Flask', '123')
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertIn('Thanks for registering!', response.data)
    
    # def test_main_page(self):
    #     """Test the main page displays"""
    #     response = self.app.get('/', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    # def test_invalid_user_registration(self):
    #     """"Registration using different passwords"""
    #     response = self.register('faithngetich188@gmail.com', 'FlaskIsAwesome')
    #     self.assertEqual(response.status_code, 200)
    #     response = self.register('faithngetich188@gmail.com', '123')
    #     self.assertIn('Sorry, Passwords must be the same!', response.data)
    
    # def test_user_invalid_email(self):
    #     """Test user has a valid email address"""
    #     response = self.register('Flask','faithngetich188@gmail.com', '123')
    #     self.assertEqual(respose.status_code, 200)
    #     response = self.register('Flask','faithngetich188@gmail.com', '123')
    #     self.assertin('Error!, Email (faithngetich188@gmail.com already exist)')

    # def test_get_request_on_bucketlist_resource(self):
    #     """Checks status code for unauthenticated user on bucketlists resource"""
    #     response = self.app.get("/v1/bucketlists/")
    #     self.assertEqual(response.status_code, 401)
    
    
    # def test_get_bucketlist(self):
    #     """Test the v1 can be read"""
    #     url = '/v1/bucketlists'
    #     response = self.test_app.get.url
    #     result = json.loads(response.data)
    #     espected = {'person1'
    #                         :{'bucketlist-0':{}, 
    #                             'bucketlist-1':
    #                                 {'item':{}, 
    #                                     'bucketlist-2': {
    #                                         'item-1': {},
    #                                         'item-2':{}, 
    #                                         'item-3': {}}}},
    #                 'person2':
    #                         {'bucketlist:1':{}},
    #                 'person3': {}}
    #     self.assertEqual(espected, response) 

    # def test_add_new_bucketlist(self):
    #     """Test that a buckectlist can be added"""
    #     q = self.db.session.querry
    #     name = 'new_goal'
    #     # verify that the goal does not exist
    #     self.assertIsNone(q(Bucketlist))
    #     params = dict(user=self.user.name, name=name)
    #     url = '/v1/bucketlists'
    #     response = self.test_app.post(url, data=params)
    #     # Response to a successful POST 
    #     self.assertEqual(200, response.status_code)
    #     self.assertIsNotNone(q(Bucketlist))

    # def test_add_an_item(self):
    #     """Test that an item is added"""
    #     q = self.db.session.querry
    #     name = 'new_bucketlist'
    #     # verify new buckectlist does not exist
    #     self.assertIsNone(q(Goal))
    #     params = dict(user=self.user.name, name=name)
    #     url = '/v1/bucketlists'
    #     response = self.test_app.post(url, data=params)
    #     self.assertEqual(200, response.status_code)
    #     parent_bucketlist = q(Goal)
    #     item_name = 'item'
    #     params = dict(user=self.user.name, name=name, parent_name=parent_bucketlist.name)
    #     response = self.test_app.post(url, data=params)
    #     self.assertEqual(200, response.status_code)
    #     item_bucketlist = q(Bucketlist)
    #     self.assertEqual(item_name, item_bucketlist.name)
    #     self.assertEqual(parent_bucketlist, item_bucketlist.name)

    # def test_complete_bucketlist(self):
    #     """Test that an item has been completed"""
    #     q = session.querry
    #     params = dict(user='person1', name='bucketlist-0')
    #     url = '/v1/bucketlists'
    #     response = self.test_app.post(url, data=params)
    #     self.assertEqual(200, response.status_code)

    #     bucketlist = q(Goal)
    #     self.assertInNone(bucketlist.Done)

    # def test_buckectlist_put_buckect_valid(self):
    #     """Test one can update the buckectlist successfully"""
    #     headers = self.get_headers_authe()
    #     json_data = {'visit the mara': 'Updated buckectlist'}
    #     response = self.app.put('/v1/users/3', data=json.dumps(json_data), headers=headers, follow_redirects=True)
    #     json_data = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('True', json_data['result'])

    def tearDown(self):
        """Tears down all test_db data and resets db to empty state"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
if __name__ == "__main__":
    unittest.main()
