#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError, Length
from movie.models import User

class RegisterForm(FlaskForm):
    name = StringField(
        label='Username',
        validators=[DataRequired('Please input user name'), Length(max=255)],
        description='Username',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'Please input username'
        }
    )

    email = StringField(
        label='mail',
        validators=[DataRequired('Please input mailbox'),
        Email('Wrong mailbox form')],
        description='mail',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'Please input mail address'
        }
    )

    phone = StringField(
        label='phone',
        validators=[DataRequired('Please input cell phone number'),
        Regexp('1[358]\\d{9}', message='cell phone form wrong')
        ],
        description='phone',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'Please input phone'
        }
    )

    pwd = StringField(
        label='Password',
        validators=[DataRequired('Please input password')],
        description='Password',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'Please input password'
        }
    )

    repwd = StringField(
        label='repassword',
        validators=[
            DataRequired('Please input repassword'),
            EqualTo('pwd', message='two different password')],
        description='repassword',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'Please input repassword'
        }
    )
    
    submit = SubmitField(
        label='Regeister',
        render_kw={
            'class':'tn btn-lg btn-success btn-block'
        }
    )

    def validate_name(self, field):
        name=field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError('name already exists')

    def validate_email(self, field):
        email=field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError('mail address already exists')
    
    def validate_phone(self, field):
        phone=field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError('phone already exists')

class LoginForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(max=255)])
    pwd = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

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
