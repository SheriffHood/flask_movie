#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Blueprint

home_blueprint = Blueprint( 'home', __name__ )

import movie.home.views