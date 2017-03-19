# -*- coding:utf-8  -*-

from app import db
from enum import Enum
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, ForeignKey

ROLE_USER = 0
ROLE_ADMIN = 1

Base = declarative_base()

#===================
class AccountType(Enum):
    L1 = 'Limited'
    L2 = 'unlimited-1'
    L3 = 'unlimited-2'
    L4 = 'unlimited-3'

class User(db.Model):
    __tablename__ = 'Customer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(20), nullable=False, unique=True) #this is login id
    last_name = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    address = db.Column(db.String(50))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zipcode = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum(AccountType) ,nullable=False, default=AccountType.L1)
    creation_data = db.Column(db.DateTime, nullable=False)
    card_num = db.Column(db.String(20))
    rating = db.Column(db.Integer)

    cart = db.relationship('Movie', secondary='Queue', backref='Customer')

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return true

    def is_active(self):
        return true

    def is_anonymous(self):
        return false

    def get_id(self):
        return self.id

    @classmethod
    def login_check(cls, user_name):
        user = cls.query.filter(db.or_(
            User.customer_id == user_name, User.customer_id == user_name)).first()

        if not user:
            return None

        return user

    def __repr__(self):
        return '<User %r>' % (self.customer_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('Customer.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)



class MovieType(Enum):
    COMEDY = 'Comedy'
    DRAMA = 'Drama'
    ACTION = 'Action'
    FOREIGN = 'Foreign'
    NA = 'N/A'  #defualt valu

class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum(MovieType), nullable=False)
    fee = db.Column(db.DECIMAL(8,2), nullable=False)
    copies = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer)

Queue = db.Table(
    'Queue',
    db.Column('customer_id', Integer, ForeignKey('Customer.id')),
    db.Column('movie_id', Integer, ForeignKey('Movie.id')),
)
