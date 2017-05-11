import os
import unittest

from app import app, db, mail


TEST_DB = 'test.db'

class BasicTests(unnitest.Testcase):
    ''' setup an teardown'''
    def setUp(self):
        app.config['TESTING']