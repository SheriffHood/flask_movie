#!/usr/bin/env python3

from flask import render_template, url_for, redirect, flash, request, session
from movie.home import home_blueprint
from movie.home.forms import LoginForm, RegisterForm
from movie.models import User, Userlog
from werkzeug.security import generate_password_hash
import uuid
from movie import db
from functools import wraps

def user_login_required(func):
    @wraps(func)
    def decorator_func(*args, **kargs):
        if 'user' not in session:
            return redirect( url_for('home.login', next=request.url) )
        return func(*args, **kargs)

    return decorator_func

@home_blueprint.route('/')
def index():
    return render_template('home/index.html')

@home_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if not user.check_pwd(data['pwd']):
            flash('Wrong password', 'err')
            return redirect(url_for('home.login'))

        session['user'] = user.name
        session['user_id'] = user.id
        
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )

        db.session.add(userlog)
        db.session.commit()
        return redirect( url_for('home.user') )
    return render_template('home/login.html', form=form)

@home_blueprint.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
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
@user_login_required
def user():
    return render_template('home/user.html')

@home_blueprint.route('/password/')
@user_login_required
def password():
    return render_template('home/password.html')

@home_blueprint.route('/comments/')
@user_login_required
def comments():
    return render_template('home/comments.html')

@home_blueprint.route('/loginlog/')
@user_login_required
def loginlog():
    return render_template('home/loginlog.html')

@home_blueprint.route('/moviecol/')
@user_login_required
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
