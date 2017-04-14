from app import db
from .models import *
from sqlalchemy.sql import func
from datetime import datetime

def getHotMovies():
    session = db.session()
    movies = session.query(Movie) \
        .order_by(Movie.NumRating, Movie.Rating) \
        .limit(10)
    return movies

def getMovies(num):
    session = db.session()
    movies = session.query(Movie).limit(num).all()
    return movies

def getMovieById(id):
    session = db.session()
    movie = session.query(Movie).filter_by(Id=id).first()
    return movie

def getHotReviews():
    session = db.session()
    reviews = session.query(Reviews) \
        .order_by(func.rand()) \
        .limit(10)
    res = []
    for r in reviews:
        res.append([r, getMovieById(r.MovieId)])
    return res

def getAccount(userId):
    session = db.session()
    account = session.query(Accounts).filter_by(Id=userId).first()
    return account

def getMovieQ(userId):
    session = db.session()
    movieQs = session.query(MovieQ).filter_by(AccountId=userId).all()
    movies = []
    for movieQ in movieQs:
        movie = getMovieById(movieQ.MovieId)
        movies.append(movie)
    return movies

def addMovieQ(userId, movieId):
    session = db.session()
    movieQ = MovieQ()
    movieQ.AccountId = userId
    movieQ.movieId = movieId
    try:
        session.add(movieQ)
        session.commint()
        return True
    except:
        session.rollback()
        return False

def getMovieF(userId):
    session = db.session()
    movieFs = session.query(MovieF).filter_by(AccountId=userId).all()
    movies = []
    for movieF in movieFs:
        movie = getMovieById(movieF.MovieId)
        movies.append(movie)
    return movies

def addMovieF(userId, movieId):
    session = db.session()
    movieF = MovieF()
    movieF.AccountId = userId
    movieF.movieId = movieId
    try:
        session.add(movieF)
        session.commint()
        return True
    except:
        session.rollback()
        return False

def getOrder(userId):
    session = db.session()
    orders = session.query(Orders).filter_by(AccountId=userId).all()
    res = []
    for order in orders:
        movie = getMovieById(order.MovieId)
        res.append([order,movie])
    return res

def addOrder(userId, movieId):
    session = db.session()
    account = getAccount(userId)
    orders = getOrder(userId)
    orders = session.query(Orders).filter_by(AccountId=userId).all()
    return None
