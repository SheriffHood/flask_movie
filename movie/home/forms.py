#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError, Length
from movie.models import User

class RegisterForm(FlaskForm):
    name = StringField('Username', [DataRequired(), Length(max=25)])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', [DataRequired(), Length(max=11)])
    password = StringField('Password', [DataRequired(), Length(min=8)])
    confirm = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    

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