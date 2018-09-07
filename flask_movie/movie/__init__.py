#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from settings import DevConfig
app.config.from_object(DevConfig)

db = SQLAlchemy(app)

from movie.models import User, Userlog, Tag, Movie, Moviecol, Preview, Comment, Auth, Role, Admin, Adminlog, Oplog

from movie.extensions import csrf
csrf.init_app(app)

from movie.admin import admin_blueprint
from movie.home import home_blueprint
   
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(home_blueprint)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404
