# -*- coding:utf-8  -*-

from app import db
from enum import Enum
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, ForeignKey

ROLE_USER = 0
ROLE_ADMIN = 1

Base = declarative_base()

###############################################################################
class Person(db.Model):
    __table__ = Table('Person', metadata, autoload=True)
class Location(db.Model):
    __table__ = Table('Location', metadata, autoload=True)
class Employee(db.Model):
    __table__ = Table('Employee', metadata, autoload=True)
class Account(db.Model):
    __table__ = Table('Account', metadata, autoload=True)
class Customer(db.Model):
    __table__ = Table('Customer', metadata, autoload=True)
class Order(db.Model):
    __table__ = Table('Order', metadata, autoload=True)
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
class Review(db.Model):
    __table__ = Table('Review', metadata, autoload=True)
