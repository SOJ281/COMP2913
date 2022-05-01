import os
import unittest
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


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

    def test_routes(self):
        print("Test routes:")
        self.assertEqual(self.app.get('/signup', follow_redirects=True).status_code, 200)
        self.assertEqual(self.app.get('/', follow_redirects=True).status_code, 200)
        self.assertEqual(self.app.get('/login', follow_redirects=True).status_code, 200)
        self.assertEqual(self.app.get('/staff', follow_redirects=True).status_code, 200)
        self.assertEqual(self.app.get('/add_scooter', follow_redirects=True).status_code, 200)
        self.assertEqual(self.app.get('/add_price', follow_redirects=True).status_code, 200)
        self.assertEqual(self.app.get('/signup', follow_redirects=True).status_code, 200)
        self.assertEqual(self.app.get('/price_view', follow_redirects=True).status_code, 200)


    def test_valid_user_registration(self):
        print("Testing registration")
        response = self.register('Scott', 19, 'scottJames44@gmail.com', 'Pa55W0rd')
        self.assertEqual(response.status_code, 200)

    def test_valid_user_login(self):
        print("Testing login")
        response = self.login('scottJames44@gmail.com', 'Pa55W0rd')
        self.assertEqual(response.status_code, 200)

    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password))
        
    def register(self, name, age, email, password):
        return self.app.post( '/signup', data=dict(name=name, age=age, email=email, password=password, pw_confirm=password), follow_redirects=True)
    
    def BookingForm(self, duration, location):
        return self.app.post('/booking', data=dict(duration=duration, location=location))

    def ScooterForm(self, available, location):
        return self.app.post('/add_scooter"', data=dict(available=available, location=location))

    def PriceForm(self, cost):
        return self.app.post('/config_price/<id>"', data=dict(cost=cost))

    def AddPriceForm(self, duration, cost):
        return self.app.post('/add_price"', data=dict(duration=duration, cost=cost))

    def CardForm(self, number, expiration_date, security_code, name, save):
        return self.app.post('/add_price"', data=dict(number=number, expiration_date=expiration_date, security_code=security_code, name=name, save=save))


if __name__ == '__main__':
    unittest.main()

    #def test_booking_routes(self):
        #with self.app:
            #print("test_booking_routes:")
            #response = self.login('fecdc@gmail.com', 'fexbex')
            #print("Results of test",self.app.post('/login', data=dict(email='fecdc@gmail.com', password='fexbex'), follow_redirects=True))

            #self.app.post.LoginForm().submit()
            #self.assertEqual(self.app.get('/booking', follow_redirects=True).status_code, 200)
