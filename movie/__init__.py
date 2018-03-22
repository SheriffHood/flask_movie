#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Flask
from settings import DevConfig
from app.admin import admin_blueprint
from app.home import home_blueprint

app = Flask(__name__)
app.config.from_object(DevConfig)

app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(home_blueprint)
