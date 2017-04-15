#-*- coding:utf-8  -*-

import os
CSRF_ENABLED = True
SECRET_KEY = '780316'

basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:781022@localhost:3306/CSE305?charset=utf8mb4'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
