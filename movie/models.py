#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from movie import app

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 'users'

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uuid = db.Column(db.String(255), unique=True)
    user_id = db.relationship('Userlog', backref='users')
 
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return  '<User %r>' % self.name

class Userlog(db.Model):

    __tablename__ = 'userlog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ip = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Userlog %r>' % self.id