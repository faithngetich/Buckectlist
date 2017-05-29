import os
import json
import unittest 
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from app.models import db
from app import create_app
from app.config import Config
from app.models.models import User, BucketList, Item



TEST_DB = 'test.db'
class TestDevelopmentConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_add_buckectlist(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "Bucketlist successfully created!")
            self.assertEqual(response.status_code, 201)

    def test_cannot_access_resource_if_not_authenticated(self):
        response = self.client.post('/api/bucketlists',
                                    content_type="application/json",)
        self.assertEqual(response.status_code, 401)

    def test_create_bucketlist_without_name(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "You did not include a bucketlist name.")
            self.assertEqual(response.status_code, 400)

    def test_add_buckectlist(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "Bucketlist successfully created!")
            self.assertEqual(response.status_code, 201)

    def test_duplicate_buckectlist(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "Bucketlist successfully created!")
            self.assertEqual(response.status_code, 201)

            # create same sbucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "Bucketlist already exists")
            self.assertEqual(response.status_code, 400)

    def test_add_item(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )

            # create item
            response = self.client.post(
                '/api/bucketlists/1/items',
                data=json.dumps(dict(
                    item_name='Trav to ernder'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "Item successfully created!")
            self.assertEqual(response.status_code, 201)

    def test_create_item_without_name(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            # create tem
            response = self.client.post(
                '/api/bucketlists/1/items',
                data=json.dumps(dict(
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "You did not include an Item name.")
            self.assertEqual(response.status_code, 400)

    def test_create_bucketlist_with_empty_name_string(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name=""
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "The bucketlist name is too short.")
            self.assertEqual(response.status_code, 400)
    
    def test_create_item_with_empty_name_string(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name=""
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            # create item
            response = self.client.post(
                '/api/bucketlists/1/items',
                data=json.dumps(dict(
                    item_name=""
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "The item name is too short.")
            self.assertEqual(response.status_code, 400)

    def test_lists_bucketlists(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "Bucketlist successfully created!")
            self.assertEqual(response.status_code, 201)

            # request for bucketlists
            response = self.client.get('/api/bucketlists', 
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
                )
            self.assertEqual(response.status_code, 200)

    def test_list_single_bucketlist(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "Bucketlist successfully created!")
            self.assertEqual(response.status_code, 201)

            # request for bucketlists
            response = self.client.get('/api/bucketlists/1', 
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
                )
            self.assertEqual(response.status_code, 200)

    def test_updates_bucketlist(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']
            
            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            # update bucket
            response = self.client.put(
                '/api/bucketlists/1',
                data=json.dumps(dict(
                    name='Travel to wendani'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)

    def test_updates_items(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']
            
            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            # update bucket
            response = self.client.put(
                '/api/bucketlists/1',
                data=json.dumps(dict(
                    name='Travel to wendani'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
        
    def test_deletes_bucketlist(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            # create item
            response = self.client.post(
                '/api/bucketlists/1/items',
                data=json.dumps(dict(
                    item_name="Read the whole bible"
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            
            # delete item
            response = self.client.delete(
                '/api/bucketlists/1/items/1',
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)

    def test_deletes_invalid_bucketlist(self):
        with self.client:
            # user register
            response = self.client.post(
                '/api/auth/register',
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
            data = json.loads(resp_register.data.decode())
            token = data['access_token']

            # create bucket
            response = self.client.post(
                '/api/bucketlists',
                data=json.dumps(dict(
                    name='Travel to bermuda'
                )),
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            
            # delete buckectlist
            response = self.client.delete(
                '/api/bucketlists/26',
                headers={"Authorization": "JWT {}".format(token)},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)

    
    def tearDown(self):
        """Tears down all test_db data and resets db to empty state"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
if __name__ == "__main__":
    unittest.main()
