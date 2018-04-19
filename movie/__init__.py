#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Flask, render_template
from settings import DevConfig
from movie.admin import admin_blueprint
from movie.home import home_blueprint
from movie.models import db
from movie.extensions import csrf


def create_app(object_name):

    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    csrf.init_app(app)
    
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(home_blueprint)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('home/404.html'), 404

    return app