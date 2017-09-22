#-*- coding:utf-8  -*-

import os
CSRF_ENABLED = True
SECRET_KEY = ''

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost:3306/CSE305?charset=utf8mb4'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
