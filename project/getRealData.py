from app import db
from app.models import *
from datetime import datetime
from faker import Factory
import random
import requests
import time, sys, traceback

num = 200
genreTypes = {}
actorIds = []
i = 300000
url = 'https://api.themoviedb.org/3/movie/'
topUrl = 'https://api.themoviedb.org/3/movie/popular'
credits = '/credits'
reviews = '/reviews'
videos = '/videos'
person = 'https://api.themoviedb.org/3/person/'
data = {'api_key' : '82874aa94b97b0e58223d1824ac7a1eb', 'language' : 'en-US'}
posterUrl = 'http://image.tmdb.org/t/p/w185'
trailerUrl = 'https://www.youtube.com/embed/'

def addAppearedIn(movieId, actorId):
    app = AppearedIn(MovieId=movieId, ActorId=actorId)
    try:
        session.add(app)
        session.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        session.rollback()

def getRate(rate, num):
    rate /= 2
    total = int(rate * num)
    star = 0
    for i in range(2,6):
        if i * num >= total:
            star = i - 1
            break
    s = total - (star * num)
    rates = [0,0,0,0,0]
    rates[star-1] = num - s
    rates[star] = s
    return rates

def getMovie(movieId):
    movieD = requests.get(url+str(movieId), data = data)
    if movieD.status_code != 200:
        return None
    movieData = movieD.json()
    rates = getRate(movieData['vote_average'], movieData['vote_count'])
    movie = Movie(Id=movieData['id'],
                   Name=movieData['title'],
                   Length=movieData['runtime'] if movieData['runtime'] else None,
                   Synopsis=movieData['overview'] if movieData['overview'] else None,
                   Language=movieData['original_language'] if movieData['original_language'] else None,
                   ReleaseDate=movieData['release_date'],
                   ImdbId=movieData['imdb_id'],
                   Num5Rating = rates[4],
                   Num4Rating = rates[3],
                   Num3Rating = rates[2],
                   Num2Rating = rates[1],
                   Num1Rating = rates[0],
                   NumCopies = random.randint(1, 1000),
                   DistrFee = random.randint(199, 9999),
                   Type=None if not movieData['genres'] else movieData['genres'][0]['name'],
                   ImageUrl=(posterUrl + movieData['poster_path']) if movieData['poster_path'] else None )
    return movie

def addActor(movieId, actorId):
    if actorId not in actorIds:
        p = requests.get(person + str(actorId), data = data)
        if p.status_code != 200:
            return
        actorData = p.json()
        actor = Actor(Id=actorData['id'],
                       Name=actorData['name'],
                       ImageUrl='' if not actorData['profile_path'] else posterUrl + actorData['profile_path'],
                       Dob=actorData['birthday'],
                       BirthPlace=actorData['place_of_birth'],
                       ImdbId=actorData['imdb_id'],
                       Rating=random.randint(10, 50),
                       NumRating=random.randint(1, 1000),
                       Biography=None if not actorData['biography'] else actorData['biography'][:1000])
        try:
            session.add(actor)
            session.commit()
            actorIds.append(actorId)
            print('===Adding Actor ', actor.Name)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            traceback.print_exc(file=sys.stdout)
            session.rollback()
    addAppearedIn(movieId, actorId)

def addActors(movie):
    c = requests.get(url + str(movie.Id) + credits, data = data)
    acts = []
    if c.status_code != 200:
        return None
    crews = c.json()['crew']
    casts = c.json()['cast']
    for crew in crews:
        if crew['job'] == 'Director':
            movie.Director = crew['name']
            addActor(movie.Id, crew['id'])
            acts.append(crew['id'])
            break
    for cast in casts:
        if cast['id'] not in acts:
            addActor(movie.Id, cast['id'])
            acts.append(cast['id'])

def addTrailer(movie):
    v = requests.get(url + str(movie.Id) + videos, data = data)
    if v.status_code != 200:
        return None
    vDatas = v.json()['results']

    for video in vDatas:
        if video['site'] == 'YouTube':
            movie.TrailerUrl = trailerUrl + video['key']
            break

def addReviews(movie):
    r = requests.get(url + str(movie.Id) + reviews, data = data)
    if r.status_code != 200:
        return None
    reviewData = r.json()['results']
    for review in reviewData:
        time.sleep(0.5)
        newReview = Reviews(Author=review['author'],
                            Content=review['content'],
                            MovieId=movie.Id,
                            AccountId=1) #long review
        try:
            session.add(newReview)
            session.commit()
            print('===Adding review ', newReview.Author)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            traceback.print_exc(file=sys.stdout)
            session.rollback()
            continue

def insert_data(page):
    topM = requests.get(topUrl, data = {'api_key' : '82874aa94b97b0e58223d1824ac7a1eb', 'language' : 'en-US', 'page' : page})

    if topM.status_code != 200:
        return
    topMovieData = topM.json()['results']
    for movieData in topMovieData:
        time.sleep(0.5)
        movie = getMovie(movieData['id'])
        if movie:
            print('===Adding movie ', movie.Name)
            try:
                session.add(movie)
                session.commit()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                traceback.print_exc(file=sys.stdout)
                session.rollback()
                continue
            addActors(movie)
            addTrailer(movie)
            addReviews(movie)

if __name__ == '__main__':
    page = 1
    session = db.session()
    while page < 10000:
        insert_data(page)
        page += 1
    print('~~~~~~~~~~~~~~Bye~~~~~')
    # movies = session.query(Movie).all()
    # size = len(movies)
    # for m in movies:
    #     print(str(m.Id) + '~~~~~~~> ' + str(size) + ' left')
    #     size -= 1
    #     if m.TrailerUrl:
    #         m.TrailerUrl.replace('watch?v=', 'embed/')
    #         session.commit()
    #     if not m.Num1Rating:
    #         m.Num1Rating = 0
    #     if not m.Num2Rating:
    #         m.Num2Rating = 0
    #     if not m.Num3Rating:
    #         m.Num3Rating = 0
    #     if not m.Num4Rating:
    #         m.Num4Rating = 0
    #     if not m.Num5Rating:
    #         m.Num5Rating = 0
    #     if m.Num1Rating < 0:
    #         m.Num1Rating *= -1
    #         m.Num1Rating += 20
    #     if m.Num2Rating < 0:
    #         m.Num2Rating *= -1
    #         m.Num2Rating += 20
    #     if m.Num3Rating < 0:
    #         m.Num3Rating *= -1
    #         m.Num3Rating += 20
    #     if m.Num4Rating < 0:
    #         m.Num4Rating *= -1
    #         m.Num4Rating += 20
    #     if m.Num5Rating < 0:
    #         m.Num5Rating *= -1
    #         m.Num5Rating += 20
    #     session.commit()
    # print('Done')
