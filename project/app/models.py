# -*- coding:utf-8  -*-

from app import db
from enum import Enum
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy import create_engine, Table, MetaData, UniqueConstraint
from sqlalchemy.orm import create_session
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
metadata = MetaData(bind=db.engine)

###############################################################################
class Person(db.Model):
    __table__ = Table('Person', metadata, autoload=True)
class Location(db.Model):
    __table__ = Table('Location', metadata, autoload=True)
class Employee(db.Model):
    __table__ = Table('Employee', metadata, autoload=True)
class Accounts(db.Model):
    __table__ = Table('Accounts', metadata, autoload=True)
class Customer(db.Model):
    __table__ = Table('Customer', metadata, autoload=True)
class Orders(db.Model):
    __table__ = Table('Orders', metadata, autoload=True)
class Movie(db.Model):
    __table__ = Table('Movie', metadata, autoload=True)
class Actor(db.Model):
    __table__ = Table('Actor', metadata, autoload=True)
class Rental(db.Model):
    __table__ = Table('Rental', metadata, autoload=True)
class MovieQ(db.Model):
    __table__ = Table('MovieQ', metadata, autoload=True)
class MovieF(db.Model):
    __table__ = Table('MovieF', metadata, autoload=True)
class AppearedIn(db.Model):
    __table__ = Table('AppearedIn', metadata, autoload=True)
class Reviews(db.Model):
    __table__ = Table('Reviews', metadata, autoload=True)
