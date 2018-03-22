#!/usr/bin/env python3

from movie.home import home_blueprint

@home_blueprint.route('/')
def index():
    return "<h1 style='color:green'>this is home</h1>"
