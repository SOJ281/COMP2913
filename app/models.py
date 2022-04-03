# file for the database
from flask_login import UserMixin
from app import db

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(100))
    age = db.Column(db.Integer)
    # staff will be pre-added to the database
    staff = db.Column(db.Boolean, default=False)
    #one-to-many relationship, a user can have multiple cards
    cards = db.relationship('CardDetails', backref='users', lazy='dynamic')
    #many-to-many relationship for booking scooters
    booking = db.relationship('Book', foreign_keys='Book.user_id', backref='users', lazy='dynamic')

    #methods for booking to be added in next sprints


class CardDetails(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(200))
    security_code = db.Column(db.String(100))
    expiration_date = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Scooters(db.Model):
    __tablename__ = 'scooters'
    id = db.Column(db.Integer, primary_key=True)
    available = db.Column(db.Integer) # 1 if available, 2 if being used
    location = db.Column(db.Integer, db.ForeignKey('locations.id'))
    booking = db.relationship('Book', backref='scooters', lazy='dynamic')

class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    #one-to-many relationship, each location might have many scooters
    #only include available scooters
    scooters = db.relationship('Scooters', backref='locations', lazy='dynamic')

#store rates and calculate price for each booking
#draft version, to be confirmed
#duration could be a primary_key ?
class Prices(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    booking = db.relationship('Book', backref='prices', lazy='dynamic')


#many-to-many relationship
#each user can book multiple scooters and each scooter can be booked by multiple users (one at a time)
class Book(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    scooter_id = db.Column(db.Integer, db.ForeignKey('scooters.id'))
    price_id = db.Column(db.Integer, db.ForeignKey('prices.id'))
    datetime = db.Column(db.DateTime)
    completed = db.Column(db.Integer) #1 if booking completed, #0 if still going on

class Feedback(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.Column(db.Text)
    priority = db.Column(db.Integer) 