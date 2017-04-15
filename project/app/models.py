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
from datetime import datetime, timedelta
import math

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

    def get_limit(self):
        if self.Type == 'Unlimited-1' or self.Type == 'Limited':
            return 1
        elif self.Type == 'Unlimited-2':
            return 2
        elif self.Type == 'Unlimited-3':
            return 3
        elif self.Type == 'Admin' or self.Type == 'CustRep':
            return 999
        return 0

    def login_check(email, password):
        session = db.session()
        account = session.query(Accounts).filter(and_(Accounts.Email == email, Accounts.PassWord==password)).first()
        print(account)
        return account

class Orders(db.Model):
    __table__ = Table('Orders', metadata, autoload=True)
    def getReturnDate(self):
        if not self.ReturnDate:
            print(type(self.OrderDate + timedelta(days=30)))
            return int((self.OrderDate + timedelta(days=30)).timestamp())
        else:
            return 0

class Movie(db.Model):
    __table__ = Table('Movie', metadata, autoload=True)
    def getRate(self):
        total = (5 * self.Num5Rating) + (4 * self.Num4Rating) + (3 * self.Num3Rating) + (2 * self.Num2Rating) + (1 * self.Num1Rating)
        num = self.Num5Rating + self.Num4Rating +self.Num3Rating + self.Num2Rating+self.Num1Rating
        if not num:
            return '0'
        return "{0:.1f}".format((total / num) * 2)

    def getStar(self):
        total = (5 * self.Num5Rating) + (4 * self.Num4Rating) + (3 * self.Num3Rating) + (2 * self.Num2Rating) + (1 * self.Num1Rating)
        num = self.Num5Rating + self.Num4Rating +self.Num3Rating + self.Num2Rating+self.Num1Rating
        if not num:
            return 0
        return math.ceil((total / num) * 2) * 5

    def sum(self):
        num = self.Num5Rating + self.Num4Rating +self.Num3Rating + self.Num2Rating+self.Num1Rating
        return num
    def percent5(self):
        num = self.Num5Rating + self.Num4Rating +self.Num3Rating + self.Num2Rating+self.Num1Rating
        return "0%" if not num else "{0:.1f}%".format(self.Num5Rating / num)
    def percent4(self):
        num = self.Num5Rating + self.Num4Rating +self.Num3Rating + self.Num2Rating+self.Num1Rating
        return "0%" if not num else "{0:.1f}%".format(self.Num4Rating / num)
    def percent3(self):
        num = self.Num5Rating + self.Num4Rating +self.Num3Rating + self.Num2Rating+self.Num1Rating
        return "0%" if not num else "{0:.1f}%".format(self.Num3Rating / num)
    def percent2(self):
        num = self.Num5Rating + self.Num4Rating +self.Num3Rating + self.Num2Rating+self.Num1Rating
        return "0%" if not num else "{0:.1f}%".format(self.Num2Rating / num)
    def percent1(self):
        num = self.Num5Rating + self.Num4Rating +self.Num3Rating + self.Num2Rating+self.Num1Rating
        return "0%" if not num else "{0:.1f}%".format(self.Num1Rating / num)
    def getActors(self):
        actors = session = db.session()
        acts = session.query(AppearedIn).filter_by(MovieId=self.Id).all()
        return actors[:5]

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
