#!/usr/bin/env python3

from flask import render_template, url_for, redirect
from movie.home import home_blueprint
from movie.home.forms import LoginForm, RegisterForm

@home_blueprint.route('/')
def index():
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
    return render_template('home/user.html')

@home_blueprint.route('/password/')
def password():
    return render_template('home/password.html')

@home_blueprint.route('/comments/')
def comments():
    return render_template('home/comments.html')

@home_blueprint.route('/loginlog/')
def loginlog():
    return render_template('home/loginlog.html')

@home_blueprint.route('/moviecol/')
def moviecol():
    return render_template('home/moviecol.html')