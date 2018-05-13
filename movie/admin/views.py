#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os, uuid
from datetime import datetime
from movie.admin import admin_blueprint
from flask import render_template, redirect, url_for, flash, session, request, current_app
from movie.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm
from movie.models import Admin, Tag, Movie, Preview, User
from functools import wraps
from movie import app, db
from werkzeug.utils import secure_filename

def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]

    return filename


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
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)

@admin_blueprint.route('/tag/del/<int:id>/', methods=['GET'])
@admin_login_required
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()

    flash("delete tag successfully", "ok")
    return redirect( url_for('admin.tag_list', page=1) )

@admin_blueprint.route('/tag/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_required
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.filter_by(id=id).first_or_404()

    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data['name'] and tag_count == 1:
            flash('Tag already exists', 'err')
            return redirect( url_for('admin.tag_edit', id=id) )
        tag.name= data['name']

        db.session.add(tag)
        db.session.commit()
        flash('Edit Tag successfully', 'ok')
        return redirect( url_for('admin.tag_edit', id=id) )
    return render_template('admin/tag_edit.html', form=form, tag=tag)
    
@admin_blueprint.route('/movie/add/', methods=['GET', 'POST'])
@admin_login_required
def movie_add():
    
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data

        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UPLOAD_PATH']):
            os.makedirs(app.config['UPLOAD_PATH'])
            os.chmod(app.config['UPLOAD_PATH'], 6)
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UPLOAD_PATH'] + url)
        form.logo.data.save(app.config['UPLOAD_PATH'] + logo)        
    
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(movie)
        db.session.commit()
        flash('Add movie successfully', 'ok')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)

@admin_blueprint.route('/movie/list/<int:page>/', methods=['GET', 'POST'])
@admin_login_required
def movie_list(page=None):

    if page is None:
        page = 1

    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/movie_list.html', page_data=page_data)

@admin_blueprint.route('/movie/del/<int:id>/', methods=['GET', 'POST'])
@admin_login_required
def movie_del(id=None):
   movie = Movie.query.get_or_404(int(id))

   db.session.delete(movie)
   db.session.commit()

   flash('Delete Movie successfully!', 'ok')
   return redirect( url_for('admin.movie_list', page=1) )

@admin_blueprint.route('/movie/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_required
def movie_edit(id=None):
    
    form = MovieForm()

    form.url.validators = []
    form.logo.validators = []

    movie = Movie.query.filter_by(id=id).first_or_404()

    if request.method == 'GET':
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star

    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data['title']).count()
        if movie_count == 1 and movie.title != data["title"]: 
            flash('Already exists!', 'err') 
            return redirect(url_for('admin.movie_edit', id=id))

        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
            os.chmod(current_app.config['UPLOAD_PATH'], 6)

        if form.url.data.filename != "":
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(current_app.config['UPLOAD_PATH']+movie.url)

        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)       
            form.logo.data.save(current_app.config['UPLOAD_PATH']+movie.logo) 

        movie.star = data['star'] 
        movie.tag_id = data['tag_id'] 
        movie.info = data['info'] 
        movie.title = data['title'] 
        movie.area = data['area'] 
        movie.length = data['length'] 
        movie.release_time = data['release_time']

        db.session.add(movie) 
        db.session.commit()

        flash('Edit Movie successfully', 'ok')
        return redirect( url_for('admin.movie_edit', id=id) )
    return render_template('admin/movie_edit.html', form=form, movie=movie)

@admin_blueprint.route('/preview/add/', methods=['GET', 'POST'])
@admin_login_required
def preview_add():

    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UPLOAD_PATH']):
            os.makedirs(app.config['UPLOAD_PATH'])
            os.chmod(app.config['UPLOAD_PATH'], 6)

        logo = change_filename(file_logo)
        form.logo.data.save(app.config['UPLOAD_PATH'] + logo)

        preview = Preview(
            title = data['title'],
            logo = logo        
        )

        db.session.add(preview)
        db.session.commit()
        flash('Add preview successfully!', 'ok')
        return redirect( url_for('admin.preview_add') )    
    return render_template('admin/preview_add.html', form=form)

@admin_blueprint.route('/preview/del/<int:id>/', methods=['GET', 'POST'])
@admin_login_required
def preview_del(id=None):
   preview = Preview.query.get_or_404(int(id))

   db.session.delete(preview)
   db.session.commit()

   flash('Delete Preview successfully!', 'ok')
   return redirect( url_for('admin.preview_list', page=1) )

@admin_blueprint.route('/preview/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_required
def preview_edit(id=None):

    form = PreviewForm()
    preview = Preview.query.get_or_404(int(id))

    if request.method == 'GET':
        form.title.data = preview.title

    if form.validate_on_submit():
        data = form.data
        
        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)       
            form.logo.data.save(current_app.config['UPLOAD_PATH']+preview.logo) 

        preview.title = data['title']

        db.session.add(preview)
        db.session.commit()
        flash('Edit preview successfully!', 'ok')
        return redirect( url_for('admin.preview_edit', id=id) )    
    return render_template('admin/preview_edit.html', form=form, preview=preview)

@admin_blueprint.route('/preview/list/<int:page>', methods=['GET', 'POST'])
@admin_login_required
def preview_list(page=None):
    
    if page is None:
        page = 1

    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/preview_list.html', page_data=page_data)

@admin_blueprint.route('/user/list/<int:page>', methods=['GET', 'POST'])
@admin_login_required
def user_list(page=None):
    
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/user_list.html', page_data=page_data)

@admin_blueprint.route('/user/del/<int:id>', methods=['GET', 'POST'])
@admin_login_required
def user_del(id=None):
    
   user = User.query.get_or_404(int(id))

   db.session.delete(user)
   db.session.commit()

   flash('Delete User successfully!', 'ok')
   return redirect( url_for('admin.user_list', page=1) )


@admin_blueprint.route('/user/view/<int:id>', methods=['GET', 'POST'])
@admin_login_required
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template('admin/user_view.html', user=user)

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
