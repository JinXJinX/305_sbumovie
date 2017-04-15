from app import db
from .models import *
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from sqlalchemy import and_
import time, sys, traceback

def getHotMovies():
    session = db.session()
    movies = session.query(Movie) \
        .order_by(Movie.Num5Rating, \
        Movie.Num4Rating, Movie.Num3Rating) \
        .limit(20)
    return movies

def getMovies(num):
    session = db.session()
    movies = session.query(Movie).limit(num).all()
    return movies

def getReviews(movieId):
    session = db.session()
    reviews = session.query(Reviews).filter_by(MovieId=movieId).all()
    return reviews

def getMovieById(id):
    session = db.session()
    movie = session.query(Movie).filter_by(Id=id).first()
    return movie

def get10MovieType():
    session = db.session()
    types = session.query(Movie.Type).group_by(Movie.Type).limit(10)
    ts = []
    for t in types:
        ts.append(t.Type)
    return ts

def getMovieByType(t, num):
    session = db.session()
    movies = session.query(Movie).filter_by(Type=t).limit(num).all()
    return movies

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
    movieQ.MovieId = movieId
    try:
        session.add(movieQ)
        session.commit()
        return True
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()
        return False

def removeMovieQ(userId, movieId):
    session = db.session()
    movieQ = session.query(MovieQ).filter_by(AccountId=userId, MovieId=movieId).first()
    try:
        movieQ.delete()
        session.commit()
        return True
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
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
    movieF.MovieId = movieId
    try:
        session.add(movieF)
        session.commit()
        return True
    except:
        session.rollback()
        return False

def removeMovieF(userId, movieId):
    session = db.session()
    movieF = session.query(MovieF).filter_by(AccountId=userId, MovieId=movieId).first()
    try:
        movieF.delete()
        session.commit()
        return True
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()
        return False

def getOrders(userId, check):
    session = db.session()
    orders = None
    if check == 0:
        orders = session.query(Orders).filter_by(AccountId=userId).filter_by(ReturnDate=None).all()
    elif check == 1:
        orders = session.query(Orders).filter_by(AccountId=userId).filter(Orders.ReturnDate!=None).all()
    movies = []
    res = []
    for order in orders:
        movie = getMovieById(order.MovieId)
        movies.append(movie)
        res.append([order, movie])
    return res, movies

def checkCurMonthOrders(userId):
    session = db.session()
    now = datetime.now()
    numOrders = session.query(Orders).filter(AccountId=userId) \
                                     .filter(extract('year', OrderDate) == now.year) \
                                     .filter(extract('month', OrderDate) == now.month) \
                                     .count()
    return numOrders

def addOrder(userId, movieId, price):
    session = db.session()
    account = getAccount(userId)
    movie = getMovieById(movieId)
    unreturnedOrders = session.query(Orders).filter_by(AccountId=userId).filter_by(ReturnDate=None).all()
    for uo in unreturnedOrders:
        if uo.MovieId == movieId:
            return 4
    print(movie.NumCopies)
    if movie.NumCopies <= 0:
        return 0
    if account.Type == 'Limited':
        num = checkCurMonthOrders(userId)
        if num >= 2:
            return 2
    limit = account.get_limit()
    if limit != 999 and unreturnedOrders >= limit:
            return 3
    try:
        order = Orders()
        order.OrderDate = datetime.now()
        order.AccountId = userId
        order.CustRepId = 1
        order.MovieId = movieId
        order.Price = price
        movie.NumCopies -= 1
        session.add(order)
        session.commit()
        return 1
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()
        return 0
    return 0

def returnMovie(userId, movieId):
    session = db.session()
    account = getAccount(userId)
    movie = getMovieById(movieId)
    unreturnedOrders = session.query(Orders).filter_by(AccountId=userId).filter_by(ReturnDate=None).all()
    for uo in unreturnedOrders:
        if uo.MovieId == movieId:
            try:
                uo.ReturnDate = datetime.now()
                movie.NumCopies += 1
                session.commit()
                return 1
            except:
                print("Unexpected error:", sys.exc_info()[0])
                traceback.print_exc(file=sys.stdout)
                session.rollback()
                return 0
    return 2 # cant find


def getActor(actorId):
    session = db.session()
    actor = session.query(Actor).filter_by(Id=actorId).first()
    return actor

def getActors(movieId):
    session = db.session()
    actIds = session.query(AppearedIn).filter_by(MovieId=movieId).limit(6).all()
    acts = []
    for actId in actIds:
        actor = getActor(actId.ActorId)
        acts.append(actor)
    return acts

def getMoviesByActorId(actorId):
    session = db.session()
    movieIds = session.query(AppearedIn).filter_by(ActorId=actorId).limit(6).all()
    movies = []
    for movId in movieIds:
        movie = session.query(Movie).filter_by(Id=movId.MovieId).first()
        movies.append(movie)
    return movies
