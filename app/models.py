from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), index = True, unique = True)
    band = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserToBand(db.Model):
    __tablename__ = 'UserToBand'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'))
    bandID = db.Column(db.Integer, db.ForeignKey('Band.id'))
    favorite = db.Column(db.Boolean)
    owns = db.Column(db.Boolean)

    def __repr__(self):
        return '<UserToBand {}>'.format(self.id)

    def __init__(self, userID, bandID, favorite, owns):
        self.userID = userID
        self.bandID = bandID
        self.favorite = favorite
        self.owns = owns

class Band(db.Model):
    __tablename__ = 'Band'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    bio = db.Column(db.String(1024))
    image = db.Column(db.String(64), unique=True)
    songLink = db.Column(db.String(64))

    def __repr__(self):
        return '<Band {}>'.format(self.id)

    def __init__(self, name, bio, image, songLink):
        self.name = name
        self.bio = bio
        self.image = image
        self.songLink = songLink


class Porch(db.Model):
    __tablename__ = 'Porch'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    events = db.relationship('Event', backref='venue', lazy='dynamic')

    def __repr__(self):
        return '<Porch {}>'.format(self.id)

    def __init__(self, address, latitude, longitude):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude


    #Should convert address into long and latitude within the function, to be figured out later when we start working with google maps API
    # def __init__(self, address):
    #     self.address = address

class Event(db.Model):
    __tablename__ = 'Event'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True)
    bandID = db.Column(db.Integer, db.ForeignKey('Band.id'))
    porchID = db.Column(db.Integer, db.ForeignKey('Porch.id'))

    def __repr__(self):
        return '<Event {}>'.format(self.id)

    def __init__(self, time, bandID, porchID):
        self.time = time
        self.bandID = bandID
        self.porchID = porchID


@login.user_loader
def user_loader(id):
    return User.query.get(int(id))