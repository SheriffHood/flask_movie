#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from movie.admin import admin_blueprint
from flask import render_template, redirect, url_for

@admin_blueprint.route('/')
def index():
    return render_template('admin/index.html')

@admin_blueprint.route('/login/')
def login():
    return render_template('admin/login.html')

@admin_blueprint.route('logout/')
def logout():
    return redirect( url_for('admin/login.html') )

@admin_blueprint.route('/password/')
def password():
    return render_template('admin/password.html')

@admin_blueprint.route('/tag/add/')
def tag_add():
    return render_template('admin/tag_add.html')

@admin_blueprint.route('/tag/list/')
def tag_list():
    return render_template('admin/tag_list.html')

@admin_blueprint.route('/movie/add/')
def movie_add():
    return render_template('admin/movie_add.html')

@admin_blueprint.route('/movie/list/')
def movie_list():
    return render_template('admin/movie_list.html')

@admin_blueprint.route('/preview/add/')
def preview_add():
    return render_template('admin/preview_add.html')

@admin_blueprint.route('/preview/list')
def preview_list():
    return render_template('admin/preview_list.html')

@admin_blueprint.route('/user/list/')
def user_list():
    return render_template('admin/user_list.html')

@admin_blueprint.route('/user/view/')
def user_view():
    return render_template('admin/user_view.html')

@admin_blueprint.route('/comment/list/')
def comment_list():
    return render_template('admin/comment_list.html')

@admin_blueprint.route('/moviecol/list')
def moviecol_list():
    return render_template('admin/moviecol_list.html')

@admin_blueprint.route('/oplog/list')
def oplog_list():
    return render_template('admin/oplog_list.html')

@admin_blueprint.route('/adminloginlog/list')
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')

@admin_blueprint.route('/userloginlog/list')
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')

@admin_blueprint.route('/role/add/')
def role_add():
    return render_template('admin/role_add.html')

@admin_blueprint.route('/role/list/')
def role_list():
    return render_template('admin/role_list.html')

@admin_blueprint.route('/auth/add/')
def auth_add():
    return render_template('admin/auth_add.html')

@admin_blueprint.route('/auth/list/')
def auth_list():
    return render_template('admin/auth_list.html')
    
@admin_blueprint.route('/admin/add/')
def admin_add():
    return render_template('admin/admin_add.html')

@admin_blueprint.route('/admin/list')
def admin_list():
    return render_template('/admin/admin_list.html')
