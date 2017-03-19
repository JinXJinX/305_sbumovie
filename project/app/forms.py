# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, BooleanField, SubmitField, TextAreaField, RadioField, IntegerField, DecimalField
from wtforms.validators import Required, Email, Length, NumberRange, URL


class LoginForm(Form):
    user_name = TextField('user name', validators=[
        Required(), Length(max=20)])
    submit = SubmitField('Log in')


class SignUpForm(Form):
    user_name = TextField('user name', validators=[
        Required(), Length(max=20)], default = 'ur name')
    user_email = TextField('user email', validators=[
        Email(), Required(), Length(max=128)])
    last_name = TextField('last name', validators=[
        Length(max=20)])
    first_name = TextField('first name', validators=[
        Length(max=20)])
    address = TextField('address', validators=[
        Length(max=50)])
    city = TextField('city', validators=[
        Length(max=20)])
    state = TextField('state', validators=[
        Length(max=20)])
    zipcode = TextField('zipcode', validators=[
        NumberRange(), Length(max=10)])
    phone = TextField('phone', validators=[
        NumberRange(), Length(max=20)])
    account_type = RadioField('Type',
                                choices=[('L1','Limited'),
                                         ('L2','unlimited-1'),
                                         ('L3','unlimited-2'),
                                         ('L4','unlimited-3')],
                                default='L1')
    submit = SubmitField('Submit!')


class PublishBlogForm(Form):
    body = TextAreaField('blog content', validators=[Required()])
    submit = SubmitField('Submit')

class PublishMovieForm(Form):
    name = TextField('Movie Name', validators=[Required()])
    movie_type = RadioField('Type',
                                choices=[('NA','N/A'),
                                         ('COMEDY','Comedy'),
                                         ('DRAMA','Drama'),
                                         ('ACTION','Action'),
                                         ('FOREIGN','Foreign')],
                                default='NA')
    #description = TextAreaField('description', validators=[Required()])
    copies = IntegerField('Number of Copies', validators=[Required()])
    fee = DecimalField('Price', validators=[Required()])
    posterUrl = TextField('Poster Url') #, validators=[URL()]
    actor1 = TextField('Actor Name')
    actor2 = TextField('Actor Name')
    actor3 = TextField('Actor Name')

    submit = SubmitField('Submit')


class AboutMeForm(Form):
    describe = TextAreaField('about me', validators=[
        Required(), Length(max=140)])
    submit = SubmitField('YES!')
