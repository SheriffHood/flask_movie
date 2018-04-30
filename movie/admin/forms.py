#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError, Length
from movie.models import User, Admin, Tag

class RegisterForm(FlaskForm):
    name = StringField('Username', [DataRequired(), Length(max=25)])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', [DataRequired(), Length(max=11)])
    password = StringField('Password', [DataRequired(), Length(min=8)])
    confirm = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    name = StringField(
        label='Username',
        validators=[DataRequired(), Length(max=255)],
        description='Username',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input username',
            'required':'required'
        }
    )

    pwd = StringField(
        label='Password',
        validators=[DataRequired()],
        description='Password',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input password',
            'required':'required'
        }
    )
    
    submit = SubmitField(
        label='Submit',
        render_kw={
            'class':'btn btn-primary btn-block btn-flat'
        }
    )

    def validate_username(self, field):
        username=field.data
        admin = Admin.query.filter_by(name=username).count
        if admin == 0:
            raise ValidationError('not exists')

class TagForm(FlaskForm):
    name = StringField(
        label='name',
        validators=[DataRequired()],
        description='Tag',
        render_kw={
            'class':'form-control',
            'id':'input_name',
            'placeholder':'Please input tags'
        }
    )

    submit = SubmitField(
        label='Submit',
        render_kw={
            'class':'btn btn-primary'
        }
    )

class MovieForm(FlaskForm):
    title = StringField(
        label='title',
        validators=[DataRequired()],
        description='Movie',
        render_kw={
            'class':'form-control',
            'id':'input_title',
            'placeholder':'Please input movie title'
        }
    )   

    url = FileField(
        label='url',
        validators=[DataRequired()],
        description='Movie files'
    )

    info = TextAreaField(
        label='information',
        validators=[DataRequired()],
        description='Movie information',
        render_kw={
            'class':'form-control',
            'row':10
        }
    )

    logo = FileField(
        label='logo',
        validators=[DataRequired()],
        description='Movie logo'
        )

    star = SelectField(
        label='star',
        validators=[DataRequired()],
        coerce=int,
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
        description='Movie star',
        render_kw={
            'class':'form-control'
        }
    )

    tag_id = SelectField(
        label='tag',
        validators=[DataRequired()],
        coerce=int,
        #choices=[ (v.id, v.name) for v in Tag.query.all() ],
        description='Movie tag',
        render_kw={
            'class':'form-control'
        }
    )

    area = StringField(
        label='area',
        validators=[DataRequired()],
        description='Movie area',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input movie area'
        }
    )

    length = StringField(
        label='length',
        validators=[DataRequired()],
        description='Movie length',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input movie length'
        }
    )

    release_time = StringField(
        label='release_time',
        validators=[DataRequired()],
        description='Movie release time',
        render_kw={
            'class': 'form-control',
            'placeholder': 'Please choose movie release time',
            'id': 'input_release_time'
        }
    )

    submit = SubmitField(
        label='Submit',
        render_kw={
            'class':'btn btn-primary'
        }
    )
    
    

class UserdetailForm(FlaskForm):
    name = StringField()
    email = StringField()
    phone = StringField()
    face = FileField()
    info = TextAreaField()
    submit = SubmitField()

class PwdForm(FlaskForm):
    old_password = PasswordField()
    new_password = PasswordField()
    submit = SubmitField()

class CommentForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(max=255)])
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
