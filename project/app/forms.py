# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, DateField, BooleanField, SubmitField, TextAreaField, RadioField, IntegerField, DecimalField
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
    city = TextField('city', validators=[
         Required(), Length(max=50)])
    state = TextField('state', validators=[
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
                                choices=[('COMEDY','Comedy'),
                                         ('DRAMA','Drama'),
                                         ('ACTION','Action'),
                                         ('FOREIGN','Foreign')],
                                default='ACTION',
                                validators=[Required()])
    #description = TextAreaField('description', validators=[Required()])
    copies = IntegerField('Number of Copies', validators=[Required()])
    language = TextField('language') #, validators=[URL()]
    length = IntegerField('movie min') #, validators=[URL()]
    director = TextField('director') #, validators=[URL()]
    synopsis = TextField('synopsis') #, validators=[URL()]
    releaseDate = DateField('date', format='%Y-%m-%d') #, validators=[URL()]
    posterUrl = TextField('Poster Url') #, validators=[URL()]
    trailerUrl = TextField('Trailer Url') #, validators=[URL()]
    imdbId = TextField('imdb Id') #, validators=[URL()]
    submit = SubmitField('Submit')

class ActorForm(Form):
    name = TextField('actor name', validators=[
        Required(), Length(max=140)])
    dob = TextField('actor name', validators=[
        Length(max=140)])
    biography = TextField('Biography') #, validators=[URL()]
    imdbId = TextField('imdbId') #, validators=[URL()]
    birthPlace = TextField('birthPlace') #, validators=[URL()]
    imageUrl = TextField('imageUrl') #, validators=[URL()]
    submit = SubmitField('YES!')

class AboutMeForm(Form):
    describe = TextAreaField('about me', validators=[
        Required(), Length(max=140)])
    submit = SubmitField('YES!')

class EmpForm(Form):
    SSN = IntegerField('SSN')
    startDate = TextField('start date', validators=[Length(max=140)])
    hourlyRate = IntegerField('houly rate (cent)')
    accountId = IntegerField('account Id', validators=[Required()])
    submit = SubmitField('SAVE')
