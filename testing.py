import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_addtaskroute(self):
        print("Test routes:")
        self.assertEqual(self.app.get('/signup', follow_redirects=True).status_code, 200)
        self.assertEqual(self.app.get('/login', follow_redirects=True).status_code, 200)

    def test_valid_user_registration(self):
        response = self.register('Scott', 19, 'scottJames44@gmail.com', 'Pa55W0rd')
        self.assertEqual(response.status_code, 200)

    def test_valid_user_login(self):
        response = self.login('scottJames44@gmail.com', 'Pa55W0rd')
        self.assertEqual(response.status_code, 200)

    def register(self, name, age, email, password):
        return self.app.post( '/signup', data=dict(name=name, age=age, email=email, password=password), follow_redirects=True)
 
    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)

if __name__ == '__main__':
    unittest.main()