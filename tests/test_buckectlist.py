import os
import unittest
from app import db
from app import create_app
from app.config import Config
from app.models.models import User, Bucketlist

class BucketlistTest(unittest.TestCase):
    # def create_app(self):
    #     app = create_app('test')
    #     return app

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
    def register(self, username, email, password):
        return self.app.post('/register', data=dict(username=username, email=email, password=password),follow_redirects=True)
    
    def login(self, email, password):
        data = dict(email=email, password=password, follow_redirects=True)
        return self.app.post('/login', data)

    def register_user(self):
        self.app.get('/register', follow_redirects=True)
        self.register('faithngetich188@gmail.com', '123')

    def logout_user(self):
        return self.app.post('/logout', follow_redirects=True)

    def add_buckectlist(self):
        self.register_user()
        user1 = User.query.filter_by(email='faithngetich188@gmail.com').first()
        bucketlist1 = Bucketlist('Travel to bermuda',user1.id, True)
        bucketlist2 = Bucketlist('Get my name to the Guinness Book of Record',user1.id, True)
        bucketlist3 = Bucketlist('Travel to Delhi',user1.id, False)
        bucketlist4 = Bucketlist('climb ',user1.id, False)
        bucketlist5 = Bucketlist('Travel to bermuda',user1.id, False)
        db.session.add(bucketlist1)
        db.session.add(bucketlist2)
        db.session.add(bucketlist3)
        db.session.add(bucketlist4)
        db.session.commit

    # Tests
    def test_valid_user_registration(self):
        response = self.register('Flask','faithngetich188@gmail.com', '123')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Thanks for registering!', response.data)
    
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_registration(self):
        """"Registartion using different passwords"""
        response = self.register('Flask','faithngetich188@gmail.com', '123')
        self.assertIn('Sorry, Passwords must be the same!', response.data)
    
    def test_user_invalid_email(self):
        response = self.register('Flask','faithngetich188@gmail.com', '123')
        self.assertEqual(respose.status_code, 200)
        response = self.register('Flask','faithngetich188@gmail.com', '123')
        self.assertin('Error!, Email (faithngetich188@gmail.com already exist)', response.data)

    def test_get_request_on_bucketlist_resource(self):
        """Checks status code for unauthenticated user on bucketlists resource"""
        response = self.app.get("/api/bucketlists/")
        self.assertEqual(response.status_code, 401)
    
    
    def test_get_bucketlist(self):
        """Test the api can be read"""
        url = '/api/bucketlists'
        response = self.test_app.get.url
        result = json.loads(response.data)
        espected = {'person1'
                            :{'bucketlist-0':{}, 
                                'bucketlist-1':
                                    {'item':{}, 
                                        'bucketlist-2': {
                                            'item-1': {},
                                            'item-2':{}, 
                                            'item-3': {}}}},
                    'person2':
                            {'bucketlist:1':{}},
                    'person3': {}}
        self.assertEqual(espected, response) 

    def test_add_new_bucketlist(self):
        """Test that a buckectlist can be added"""
        q = self.db.session.querry
        name = 'new_goal'
        # verify that the goal does not exist
        self.assertIsNone(q(Bucketlist))
        params = dict(user=self.user.name, name=name)
        url = '/api/bucketlists'
        response = self.test_app.post(url, data=params)
        # Response to a successful POST 
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(q(Bucketlist))

    def test_add_nested_bucketlists(self):
        """Test that an item is added"""
        q = self.db.session.querry
        name = 'new_bucketlist'
        # verify new buckectlist does not exist
        self.assertIsNone(q(Goal))
        params = dict(user=self.user.name, name=name)
        url = '/api/bucketlists'
        response = self.test_app.post(url, data=params)
        self.assertEqual(200, response.status_code)
        parent_bucketlist = q(Goal)
        item_name = 'item'
        params = dict(user=self.user.name, name=name, parent_name=parent_bucketlist.name)
        response = self.test_app.post(url, data=params)
        self.assertEqual(200, response.status_code)
        item_bucketlist = q(Bucketlist)
        self.assertEqual(item_name, item_bucketlist.name)
        self.assertEqual(parent_bucketlist, item_bucketlist.name)

    def test_complete_bucketlist(self):
        """Test that an item has been completed"""
        q = session.querry
        params = dict(user='person1', name='bucketlist-0')
        url = '/v1.0/bucketlists'
        response = self.test_app.post(url, data=params)
        self.assertEqual(200, response.status_code)

        bucketlist = q(Goal)
        self.assertInNone(bucketlist.Done)

    def test_recipes_api_put_buckect_valid(self):
        """Test one can update the buckectlist successfully"""
        headers = self.get_headers_authenticated_admin()
        json_data = {'visit the mara': 'Updated buckectlist'}
        response = self.app.put('/api/users/3', data=json.dumps(json_data), headers=headers, follow_redirects=True)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('True', json_data['result'])
