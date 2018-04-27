#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from movie.admin import admin_blueprint
from flask import render_template, redirect, url_for, flash, session, request
from movie.admin.forms import LoginForm, TagForm
from movie.models import Admin, Tag
from functools import wraps
from movie.models import db

def admin_login_required(func):
    @wraps(func)
    def decorator_func(*args, **kargs):
        if 'admin' not in session:
            return redirect( url_for('admin.login', next=request.url) )
        return func(*args, **kargs)
    return decorator_func

@admin_blueprint.route('/')
@admin_login_required
def index():
    return render_template('admin/index.html')

@admin_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['name']).first()
        if not admin.check_pwd(data['pwd']):
            flash('wrong password')
            return redirect( url_for('admin.login') )
        session['admin'] = data['name']
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)

@admin_blueprint.route('/logout/', methods=['GET', 'POST'])
@admin_login_required
def logout():
    session.pop('admin', None)
    return redirect( url_for('admin/login.html') )

@admin_blueprint.route('/password/')
@admin_login_required
def password():
    return render_template('admin/password.html')

@admin_blueprint.route('/tag/add/', methods=['GET', 'POST'])
@admin_login_required
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash('Tag already exists', 'err')
            return redirect( url_for('admin.tag_add') )
        tag = Tag(name = data['name'])
        db.session.add(tag)
        db.session.commit()
        flash('Create Tag successfully', 'ok')
        return redirect( url_for('admin.tag_add') )
    return render_template('admin/tag_add.html', form=form)

@admin_blueprint.route('/tag/list/<int:page>/', methods=['GET'])
@admin_login_required
def tag_list(page):
    if page == None:
        page = 1
    page_data = Tag.query.order_by(Tag.addtime.desc()).paginate(page=page, per_page=1)
    return render_template('admin/tag_list.html', page_data=page_data)

@admin_blueprint.route('/movie/add/')
@admin_login_required
def movie_add():
    return render_template('admin/movie_add.html')

@admin_blueprint.route('/movie/list/')
@admin_login_required
def movie_list():
    return render_template('admin/movie_list.html')

@admin_blueprint.route('/preview/add/')
@admin_login_required
def preview_add():
    return render_template('admin/preview_add.html')

@admin_blueprint.route('/preview/list')
@admin_login_required
def preview_list():
    return render_template('admin/preview_list.html')

@admin_blueprint.route('/user/list/')
@admin_login_required
def user_list():
    return render_template('admin/user_list.html')

@admin_blueprint.route('/user/view/')
@admin_login_required
def user_view():
    return render_template('admin/user_view.html')

@admin_blueprint.route('/comment/list/')
@admin_login_required
def comment_list():
    return render_template('admin/comment_list.html')

@admin_blueprint.route('/moviecol/list')
@admin_login_required
def moviecol_list():
    return render_template('admin/moviecol_list.html')

@admin_blueprint.route('/oplog/list')
@admin_login_required
def oplog_list():
    return render_template('admin/oplog_list.html')

@admin_blueprint.route('/adminloginlog/list')
@admin_login_required
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')

@admin_blueprint.route('/userloginlog/list')
@admin_login_required
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')

@admin_blueprint.route('/role/add/')
@admin_login_required
def role_add():
    return render_template('admin/role_add.html')

@admin_blueprint.route('/role/list/')
@admin_login_required
def role_list():
    return render_template('admin/role_list.html')

@admin_blueprint.route('/auth/add/')
@admin_login_required
def auth_add():
    return render_template('admin/auth_add.html')

@admin_blueprint.route('/auth/list/')
@admin_login_required
def auth_list():
    return render_template('admin/auth_list.html')
    
@admin_blueprint.route('/admin/add/')
@admin_login_required
def admin_add():
    return render_template('admin/admin_add.html')

@admin_blueprint.route('/admin/list')
@admin_login_required
def admin_list():
    return render_template('/admin/admin_list.html')
