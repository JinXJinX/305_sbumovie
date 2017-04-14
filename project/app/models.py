# -*- coding:utf-8  -*-

from app import db
from enum import Enum
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy import create_engine, Table, MetaData, UniqueConstraint
from sqlalchemy.orm import create_session
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import and_
metadata = MetaData(bind=db.engine)

###############################################################################
class Location(db.Model):
    __table__ = Table('Location', metadata, autoload=True)

class Employee(db.Model):
    __table__ = Table('Employee', metadata, autoload=True)

class Accounts(db.Model):
    __table__ = Table('Accounts', metadata, autoload=True)
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_admin(self):
        return self.Type == 'Admin' or self.Type == 'CustRep'

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.Id

    def login_check(email, password):
        session = db.session()
        account = session.query(Accounts).filter(and_(Accounts.Email == email, Accounts.PassWord==password)).first()
        print(account)
        return account

class Orders(db.Model):
    __table__ = Table('Orders', metadata, autoload=True)

class Movie(db.Model):
    __table__ = Table('Movie', metadata, autoload=True)

class Actor(db.Model):
    __table__ = Table('Actor', metadata, autoload=True)

class MovieQ(db.Model):
    __table__ = Table('MovieQ', metadata, autoload=True)

class MovieF(db.Model):
    __table__ = Table('MovieF', metadata, autoload=True)

class AppearedIn(db.Model):
    __table__ = Table('AppearedIn', metadata, autoload=True)

class Reviews(db.Model):
    __table__ = Table('Reviews', metadata, autoload=True)
