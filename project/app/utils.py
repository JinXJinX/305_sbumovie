# -*- coding:utf-8 -*-

from app import db
from .models import *
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from sqlalchemy import and_
import time, sys, traceback
from sqlalchemy.sql.expression import extract
from collections import Counter
from math import ceil
PER_PAGE = 20

def getHotMovies():
    session = db.session()
    movies = session.query(Movie) \
        .filter(Movie.ReleaseDate < '{0:%Y-%m-%d}'.format(datetime.now())) \
        .order_by(Movie.ReleaseDate.desc()) \
        .limit(20)
    return movies

def getReviews(movieId):
    session = db.session()
    reviews = session.query(Reviews).filter_by(MovieId=movieId).all()
    return reviews

def getLocation(zipcode):
    session = db.session()
    location = session.query(Location).filter_by(ZipCode=zipcode).first()
    return location

def getReviewById(reviewId):
    session = db.session()
    review = session.query(Reviews).filter_by(Id=reviewId).first()
    return review

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
    try:
        session.query(MovieQ).filter_by(AccountId=userId, MovieId=movieId).delete()
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
    try:
        session.query(MovieF).filter_by(AccountId=userId, MovieId=movieId).delete()
        session.commit()
        return True
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()
        return False

def getMovieR(userId):
    session = db.session()
    movieRs = session.query(MovieR).filter_by(AccountId=userId).all()
    movies = []
    for movieR in movieRs:
        movie = getMovieById(movieR.MovieId)
        movies.append(movie)
    return movies

def addMovieR(userId, movieId):
    session = db.session()
    movieR = MovieR()
    movieR.AccountId = userId
    movieR.MovieId = movieId
    try:
        session.add(movieR)
        session.commit()
        return True
    except:
        session.rollback()
        return False

def removeMovieR(userId, movieId):
    session = db.session()
    try:
        session.query(MovieR).filter_by(AccountId=userId, MovieId=movieId).delete()
        session.commit()
        return True
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()
        return False

def getMovies(num, userId = None):
    session = db.session()
    if not userId:
        movies = session.query(Movie).limit(num).all()
        return movies
    else:
        movies = getMovieR(userId)
        if len(movies) < num:
            fmovies = getMovieF(userId)
            types = []
            for fm in fmovies:
                types.append(fm.Type)
            c = Counter(types)
            n = num - len(movies)
            l = len(types)
            for k, v in c.items():
                movies.extend(session.query(Movie)\
                                .filter_by(Type=k)\
                                .order_by(Movie.Num5Rating.desc(), Movie.Num4Rating.desc(), Movie.Num3Rating.desc())\
                                .limit(ceil(v / l * n)).all())
            if len(movies) < num:
                movies.extend(session.query(Movie).limit(num - len(movies)).all())

        return movies if len(movies) <= num else movies[:num]

def getOrders(userId, check):
    session = db.session()
    orders = None
    if check == 0:
        orders = session.query(Orders).filter_by(AccountId=userId).filter_by(ReturnDate=None).all()
    elif check == 1:
        orders = session.query(Orders).filter_by(AccountId=userId).filter(Orders.ReturnDate!=None).order_by(Orders.ReturnDate.desc()).all()
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
    numOrders = session.query(Orders).filter_by(AccountId=userId) \
                                     .filter(extract('year', Orders.OrderDate) == now.year) \
                                     .filter(extract('month', Orders.OrderDate) == now.month).all()
    return len(numOrders)

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
    if limit != 999 and len(unreturnedOrders) >= limit:
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

def dataSearch(str):
    str = str.lower()
    session = db.session()
    words = str.split()
    movies = []
    actors = []
    ms = session.query(Movie).filter(Movie.Name == str).all()
    movies.extend(ms)
    q =  str
    ms = session.query(Movie).filter(Movie.Name.like(q)).all()
    movies.extend(ms)
    # ms = session.query(Movie).filter(Movie.Synopsis.like(q)).all()
    # movies.extend(ms)
    acts = session.query(Actor).filter(Actor.Name.like(q)).all()
    actors.extend(acts)
    # acts = session.query(Actor).filter(Actor.Biography.like(q)).all()
    # actors.extend(acts)
    for word in words:
        q = '%' + word + '%'
        ms = session.query(Movie).filter(Movie.Name.like(q)).all()
        movies.extend(ms)
        # ms = session.query(Movie).filter(Movie.Synopsis.like(q)).all()
        # movies.extend(ms)
        acts = session.query(Actor).filter(Actor.Name.like(q)).all()
        actors.extend(acts)
        # acts = session.query(Actor).filter(Actor.Biography.like(q)).all()
        # actors.extend(acts)
    return list(set(movies))[:20], list(set(actors))[:20]

#Actions for admin user
def getAddress(user_id):
    session = db.session()
    acc = getAccount(user_id)
    if acc.ZipCode:
        location = getLocation(acc.ZipCode)
        return acc.FirstName + ' ' + acc.LastName + '\\n' + \
                acc.Address + ',\\n' + location.City + ', ' + \
                location.State + ', ' + str(acc.ZipCode) + '\\nUS'
    else:
        return "EMPTY"

def getUsers(page):
    num = 20
    session = db.session()
    accounts = session.query(Accounts).limit(num * page).all()
    accs = accounts[num * (page - 1) : (num * page)]
    res = []
    for acc in accs:
        res.append([acc, getAddress(acc.Id)])
    return res

def getMostActiveUsers(page):
    num = 20
    session = db.session()
    #userIds = session.query(Orders.AccountId).distinct()
    qs = session.query(Orders.AccountId, func.count(Orders.AccountId).label('total')).group_by(Orders.AccountId).order_by('total DESC')
    accounts = []
    for q in qs:
        accounts.append(getAccount(q.AccountId))
    #return accounts[num * (page - 1) : (num * page)]
    accs = accounts[num * (page - 1) : (num * page)]
    res = []
    for acc in accs:
        res.append([acc, getAddress(acc.Id)])
    return res

def getMostActiveMovies(page):
    num = 20
    session = db.session()
    qs = session.query(Orders.MovieId, func.count(Orders.MovieId).label('total')).group_by(Orders.MovieId).order_by('total DESC')
    movies = []
    for q in qs:
        movies.append(getMovieById(q.MovieId))
    return movies[num * (page - 1) : (num * page)]

def delUser(userId):
    session = db.session()
    try:
        account = session.query(Accounts).filter_by(Id = userId).first()
        session.delete(account)
        session.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()

def delMovie(movieId):
    session = db.session()
    session.query(AppearedIn).filter_by(MovieId = movieId).delete()
    session.query(Reviews).filter_by(MovieId = movieId).delete()
    session.commit()
    try:
        session.query(Movie).filter_by(Id = movieId).delete()
        session.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()

def delActor(actorId):
    session = db.session()
    session.query(AppearedIn).filter_by(ActorId = actorId).delete()
    session.commit()
    try:
        session.query(Actor).filter_by(Id = actorId).delete()
        session.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()

def getEmployees(page):
    num = 20
    session = db.session()
    emps = session.query(Employee).limit(num * page).all()
    res = []
    for emp in emps:
        acc = getAccount(emp.AccountId)
        res.append([emp, acc])
    return res[num * (page - 1) : (num * page)]

def getOrdersList(page):
    num = 20
    session = db.session()
    orders = session.query(Orders).limit(num * page).all()
    return orders[num * (page - 1) : (num * page)]

def getMoviesList(page):
    num = 20
    session = db.session()
    movies = session.query(Movie).limit(num * page).all()
    return movies[num * (page - 1) : (num * page)]

def getActorsList(page):
    num = 20
    session = db.session()
    actors = session.query(Actor).limit(num * page).all()
    return actors[num * (page - 1) : (num * page)]

def upgradeToCustRep(user_id):
    session = db.session()
    account = session.query(Accounts).filter_by(Id = user_id).first()
    account.Type = 'CustRep'
    emp = Employee()
    emp.StartDate = datetime.now()
    emp.AccountId = user_id
    session.add(emp)
    try:
        session.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()

def upgradeToAdmin(user_id):
    session = db.session()
    account = getAccount(user_id)
    account.Type = 'Admin'
    try:
        session.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()
