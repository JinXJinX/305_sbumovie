from app import db
from .models import ( Person, Movie)
from datetime import datetime

def getHotMovies():
    session = db.session()
    movies = session.query(Movie).limit(10).order_by(Movie.NumRating, Movie.Rating)
    return moveis


if __name__ == '__main__':
    print(getHotMovies)
