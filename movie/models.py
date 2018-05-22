#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from datetime import datetime
from werkzeug.security import check_password_hash

from movie import db

class User(db.Model):

    __tablename__ = 'users'

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)

    userlogs = db.relationship('Userlog', backref='users')
    comments = db.relationship('Comment', backref='users')
    moviecols = db.relationship('Moviecol', backref='users')
 
    #def __init__(self, name):
        #self.name = name

    def __repr__(self):
        return  '<User %r>' % self.name

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)

class Userlog(db.Model):

    __tablename__ = 'userlog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ip = db.Column(db.String(255))
    loggin_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Userlog %r>' % self.id

class Tag(db.Model):

    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    movies = db.relationship('Movie', backref='tag')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % self.name

class Movie(db.Model):

    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255))
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    comments = db.relationship('Comment', backref='movie')
    moviecols = db.relationship('Moviecol', backref='movie')

    def __init__(self, title, url, info, logo, star, playnum, commentnum, tag_id, area, release_time, length):
        self.title = title
        self.url = url
        self.logo = logo
        self.star = star
        self.playnum = playnum
        self.commentnum = commentnum
        self.tag_id = tag_id
        self.area = area
        self.release_time = release_time
        self.length = length

    def __repr__(self):
        return '<Movie %r>' % self.title

class Preview(db.Model):
    
    __tablename__ = 'preview'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __init__(self, title, logo):
        self.title = title
        self.logo = logo

    def __repr__(self):
        return '<Preview %r>' % self.title

class Comment(db.Model):
    
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.Text)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id  = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Comment %r>' % self.id

class Moviecol(db.Model):

    __tablename__ = 'moviecols'

    id = db.Column(db.Integer, primary_key=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Moviecol %r>' % self.id

class Auth(db.Model):

    __tablename__ = 'auth'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr_(self):
        return '<Auth %r>' % self.name

class Role(db.Model):

    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.String(255), index=True, default=datetime.now)

    admins = db.relationship('Admin', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class Admin(db.Model):
    
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    addtime = db.Column(db.String(255), index=True, default=datetime.now)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    adminlogs = db.relationship('Adminlog', backref='admin')
    oplogs = db.relationship('Oplog', backref='admin')

    def __repr__(self):
        return '<Admin %r>' % self.name
        
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)

class Adminlog(db.Model):
    
    __tablename__ = 'adminlog'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    addtime = db.Column(db.String(255), index=True, default=datetime.now)

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return '<Adminlog %r>' % self.id

class Oplog(db.Model):
    
    __tablename__ = 'oplog'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    addtime = db.Column(db.String(255), index=True, default=datetime.now)
    reason = db.Column(db.String(600))

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return '<Oplog %r>' % self.id
