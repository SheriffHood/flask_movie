#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from movie.admin import admin_blueprint

@admin_blueprint.route('/')
def index():
    return "<h1 style='color:red'>this is admin</h1>"
