#!/usr/bin/env python3

from flask import render_template, url_for, redirect, flash
from movie.home import home_blueprint
from movie.home.forms import LoginForm, RegisterForm
from movie.models import User
from werkzeug.security import generate_password_hash
import uuid
from movie import db

@home_blueprint.route('/')
def index():
    return render_template('home/index.html')

@home_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('home/login.html')

@home_blueprint.route('/logout/', methods=['GET', 'POST'])
def logout():
    return redirect( url_for('home.login') )

@home_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
            uuid = uuid.uuid4().hex
            
        )
        db.session.add(user)
        db.session.commit()
        flash('Add user successfullly!', 'ok')
    return render_template('home/register.html', form=form)

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

@home_blueprint.route('/animation/')
def animation():
    return render_template('/home/animation.html')

@home_blueprint.route('/search/')
def search():
    return render_template('home/search.html')

@home_blueprint.route('/play/')
def play():
    return render_template('home/play.html')
