#!/usr/bin/env python3

from app.home import home_blueprint

@home_blueprint.route('/')
def index():
    return "<h1 style='color':red>this is home</h1>"
