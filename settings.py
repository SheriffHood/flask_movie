#!/usr/bin/env python3
#-*- coding:utf-8 -*-

class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
