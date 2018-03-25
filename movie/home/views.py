#!/usr/bin/env python3

from flask import render_template, url_for, redirect
from movie.home import home_blueprint

@home_blueprint.route('/')
def index():
    return render_template('home/index.html')

@home_blueprint.route('/login/')
def login():
    return render_template('home/login.html')

@home_blueprint.route('/logout/')
def logout():
    return redirect( url_for('home.login') )

@home_blueprint.route('/register/')
def register():
    return render_template('home/register.html')

@home_blueprint.route('/user/', methods=['GET', 'POST'])
def user():
    pass

@home_blueprint.route('/serach/<int:page>/')
def search(page=None):
    pass