from app import db

from app.models import User, Movie
from app.models import AccountType, MovieType
from datetime import datetime

def insert_data():
    #CUSTOMER TABLE
    user = User()
    user.id = 4
    user.customer_id = "111111111"
    user.last_name = "Yang"
    user.first_name = "Shang"
    user.address = "123 Success Street"
    user.city = "Stony Brook"
    user.state = "NY"
    user.zipcode = "11790"
    user.phone = "5166328959"
    user.email = "syang@cs.sunysb.edu"
    user.type = AccountType.L1
    user.creation_data = "2017-05-05"
    user.card_num = "1234567812345670"
    user.rating = 1
    db.session.add(user)
    db.session.commit()

    user = User()
    user.id = 2
    user.customer_id = "222222222"
    user.last_name = "Du"
    user.first_name = "Victor"
    user.address = "456 Fortune Road"
    user.city = "Stony Brook"
    user.state = "NY"
    user.zipcode = "11790"
    user.phone = "5166324360"
    user.email = "vicdu@cs.sunysb.edu"
    user.type = AccountType.L1
    user.creation_data = "2006-10-15"
    user.card_num = "5678123456781230"
    user.rating = 1
    db.session.add(user)
    db.session.commit()

    user = User()
    user.id = 3
    user.customer_id = "333333333"
    user.last_name = "Smith"
    user.first_name = "John"
    user.address = "789 Peace Blvd"
    user.city = "Los Angeles"
    user.state = "CA"
    user.zipcode = "93536"
    user.phone = "3154434321"
    user.email = "jsmith@ic.sunysb.edu"
    user.type = AccountType.L1
    user.creation_data = "2017-03-15"
    user.card_num = "2345678923456780"
    user.rating = 1
    db.session.add(user)
    db.session.commit()

    user = User()
    user.id = 1
    user.customer_id = "444444444"
    user.last_name = "Philip"
    user.first_name = "Lewis"
    user.address = "135 Knowledge Lane"
    user.city = "Stony Brook"
    user.state = "NY"
    user.zipcode = "11790"
    user.phone = "5166668888"
    user.email = "pml@cs.sunysb.edu"
    user.type = AccountType.L3
    user.creation_data = "2006-10-01"
    user.card_num = "6789234567892340"
    user.rating = 1
    db.session.add(user)
    db.session.commit()

    #MOVIE TABLE
    movie = Movie()
    movie.id = 1
    movie.movie_name = "The Godfather"
    movie.type = MovieType.DRAMA
    movie.fee = 10000
    movie.copies = 3
    movie.rating = 5
    db.session.add(movie)
    db.session.commit()

    movie = Movie()
    movie.id = 2
    movie.movie_name = "Shawshank Redemption"
    movie.type = MovieType.DRAMA
    movie.fee = 1000
    movie.copies = 2
    movie.rating = 4
    db.session.add(movie)
    db.session.commit()

    movie = Movie()
    movie.id = 3
    movie.movie_name = "Borat"
    movie.type = MovieType.COMEDY
    movie.fee = 500
    movie.copies = 1
    movie.rating = 3
    db.session.add(movie)
    db.session.commit()
