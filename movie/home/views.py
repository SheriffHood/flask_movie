#!/usr/bin/env python3

from flask import render_template, url_for, redirect, flash, request, session
from movie.home import home_blueprint
from movie.home.forms import LoginForm, RegisterForm, UserdetailForm, PwdForm
from movie.models import User, Userlog
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid, os
from movie import db, app
from datetime import datetime
from functools import wraps

def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]

    return filename

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
    
    form = UserdetailForm()
    user = User.query.get(int(session['user_id']))
    form.face.validators = []
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        file_face = secure_filename(form.face.data.filename)
        if not os.path.exists(app.config['FACE_PATH']):
            os.makedirs(app.config['FACE_PATH'])
            os.chmod(app.config['FACE_PATH'], 6)

        user.face = change_filename(file_face)
        form.face.data.save(app.config['FACE_PATH'] + user.face)

        name_count = User.query.filter_by(name=data['name']).count()
        if data['name'] != user.name and name_count == 1:
            flash('name already exists', 'err')
            return redirect(url_for('home.user'))

        email_count = User.query.filter_by(email=data['email']).count()
        if data['email'] != user.email and email_count == 1:
            flash('email already exists', 'err')
            return redirect(url_for('home.user'))

        phone_count = User.query.filter_by(phone=data['phone']).count()
        if data['phone'] != user.phone and phone_count == 1:
            flash('phone already exists', 'err')
            return redirect(url_for('home.user'))

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']

        db.session.add(user)
        db.session.commit()
        flash('Revise user successfully!', 'ok')
        return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, user=user)

@home_blueprint.route('/password/', methods=['GET', 'POST'])
@user_login_required
def password():
    
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first()
        if not user.check_pwd(data['old_password']):
            flash('Wrong old password', 'err')
            return redirect(url_for('home.password')) 
        user.pwd = generate_password_hash(data['new_password'])

        db.session.add(user)
        db.session.commit()
        flash('Reset password successfully!', 'ok')
        return redirect(url_for('home.logout'))
    return render_template('home/password.html', form=form)
    

    return render_template('home/password.html')

@home_blueprint.route('/comments/')
@user_login_required
def comments():
    return render_template('home/comments.html')

@home_blueprint.route('/loginlog/<int:page>/', methods=['GET', 'POST'])
@user_login_required
def loginlog(page=None):
    
    if page is None:
        page = 1

    page_data = Userlog.query.filter_by(
        user_id = int( session['user_id'] )
    ).order_by(
        Userlog.loggin_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)

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
