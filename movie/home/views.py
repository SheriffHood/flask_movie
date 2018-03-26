#!/usr/bin/env python3

from flask import render_template, url_for, redirect
from movie.home import home_blueprint
from movie.home.forms import LoginForm, RegisterForm

@home_blueprint.route('/')
def index():
<<<<<<< HEAD
    return "<h1 style='color:green'>this is home</h1>"
=======
    return render_template('home/index.html')

@home_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass  
    return render_template('home/login.html', form=form)

@home_blueprint.route('/logout/', methods=['GET', 'POST'])
def logout():
    return redirect( url_for('home.login') )

@home_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    return render_template('home/register.html')

@home_blueprint.route('/user/', methods=['GET', 'POST'])
def user():
    pass

@home_blueprint.route('/serach/<int:page>/')
def search(page=None):
    pass
<<<<<<< HEAD
>>>>>>> enzo
=======
>>>>>>> enzo
