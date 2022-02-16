# file for the database

from app import db

# basic models for now, relationships to be added later
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(100))
    age = db.Column(db.Integer)
    #card details - have a separate model ?
    #booking = will have a relationship with Scooters via the Bookings model

class Scooters(db.Model):
    __tablename__ = 'scooters'
    id = db.Column(db.Integer, primary_key=True)
    available = db.Column(db.Integer) # 0 if available, 1 if being used
    # location - will have a relationship with the Location model

class Locations(db.Models):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    # available scooters - will have a relationship with the Scooters model

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(100))

class Bokings(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    # other fields will come from Users-Scooters relationship

#store rates and calculate price for each booking
#draft version, to be confirmed
class Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer)
    cost = db.Column(db.Integer)

