# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, BooleanField, SubmitField, TextAreaField, RadioField, IntegerField, DecimalField
from wtforms.validators import Required, Email, Length, NumberRange, URL

class LoginForm(Form):
    user_email = TextField('user email', validators=[
        Required(), Length(max=60)])
    user_password = TextField('password', validators=[
        Required(), Length(max=20)])
    submit = SubmitField('Log in')

class SearchForm(Form):
    query = TextField('', validators=[
        Required(), Length(max=200)])
    submit = SubmitField('Search')

class SignUpForm(Form):
    user_email = TextField('user email', validators=[
        Email(), Required(), Length(max=128)])
    user_password = TextField('pass word', validators=[
        Required(), Length(max=20)])
    user_name = TextField('user name', validators=[
        Length(max=20)])
    last_name = TextField('last name', validators=[
         Required(), Length(max=20)])
    first_name = TextField('first name', validators=[
         Required(), Length(max=20)])
    credit_card = TextField('credit card number', validators=[
         Required(), Length(max=20)])
    address = TextField('address', validators=[
         Required(), Length(max=50)])
    zipcode = TextField('zipcode', validators=[
         Required(), NumberRange(), Length(max=10)])
    phone = TextField('phone', validators=[
         Required(), NumberRange(), Length(max=20)])
    account_type = RadioField('Type',
                                choices=[('Limited','Limited Plan $10/month'),
                                         ('Unlimited-1','Unlimited-1 Plan $15/month'),
                                         ('Unlimited-2','Unlimited-2 Plan $20/month'),
                                         ('Unlimited-3','Unlimited-3 Plan $25/month')],
                                default='Limited')
    submit = SubmitField('Submit!')


class PublishBlogForm(Form):
    body = TextAreaField('write rate', validators=[Required()])
    rate = RadioField('Rate', choices=[('1','1&#9733&nbsp&nbsp'),
                                         ('2','2&#9733&nbsp&nbsp'),
                                         ('3','3&#9733&nbsp&nbsp'),
                                         ('4','4&#9733&nbsp&nbsp'),
                                         ('5','5&#9733&nbsp&nbsp')],
                                default='1')
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

class ActorForm(Form):
    name = TextField('actor name', validators=[
        Required(), Length(max=140)])
    age = TextField('actor name', validators=[
        Required(), Length(max=140)])
    type = TextField('actor name', validators=[
        Required(), Length(max=140)])
    dob = TextField('actor name', validators=[
        Required(), Length(max=140)])
    submit = SubmitField('YES!')

class AboutMeForm(Form):
    describe = TextAreaField('about me', validators=[
        Required(), Length(max=140)])
    submit = SubmitField('YES!')
