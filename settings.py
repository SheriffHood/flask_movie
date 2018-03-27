#!/usr/bin/env python3
#-*- coding:utf-8 -*-

class Config(object):
    SECRET_KEY = 'ode7oyfn434nvhxp9tfaw5gnc6mogkg3'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/movie'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True