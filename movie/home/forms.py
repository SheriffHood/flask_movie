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
    name = StringField(
        label='Username',
        validators=[DataRequired('Please input user name'), Length(max=255)],
        description='Username',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'Please input username'
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
    
    submit = SubmitField(
        label='Regeister',
        render_kw={
            'class':'tn btn-lg btn-success btn-block'
        }
    )

class UserdetailForm(FlaskForm):
    name = StringField(
        label='Username',
        validators=[DataRequired('Please input user name'), Length(max=255)],
        description='Username',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input username'
        }
    )

    email = StringField(
        label='mail',
        validators=[DataRequired('Please input mailbox'),
        Email('Wrong mailbox form')],
        description='mail',
        render_kw={
            'class':'form-control',
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
            'class':'form-control',
            'placeholder':'Please input phone'
        }
    )

    face = FileField(
        label='face',
        validators=[DataRequired('Please upload face')],
        description='face'
        )

    info = TextAreaField(
        label='info',
        validators=[DataRequired('Please input user info')],
        description='info',
        render_kw={
            'class':'form-control',
            'rows':10
        }
    )

    submit = SubmitField(
        label='Save',
        render_kw={
            'class':'btn btn-success'
        }
    )

class PwdForm(FlaskForm):

    old_password = PasswordField(
    label='old password',
    validators=[DataRequired('Please input old password')],
    description='old_password',
    render_kw={
        'class':'form-control',
        'placeholder':'Please input old password'
        }
    )

    new_password = PasswordField(
        label='new password',
        validators=[DataRequired('Please input new password')],
        description='new_password',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input new password'
        }
    )

    submit = SubmitField(
        label='Reset password',
        render_kw={
            'class':'btn btn-success',
        }
    )

class CommentForm(FlaskForm):
    context = TextAreaField(
        label='内容',
        validators=[DataRequired('Please input comment')],
        description='内容',
        render_kw={
            'id':'input_content'
        }
    )
    submit = SubmitField(
        label='Submit_Comment',
        render_kw={
            'class':'btn btn-success',
            'id':'btn-sub'
        }
    )
