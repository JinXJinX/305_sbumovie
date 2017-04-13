from app import db
from app.models import Person, Location, Movie, Employee, Accounts, Customer, Orders, Actor, Rental, MovieQ, MovieF, AppearedIn, Reviews
from datetime import datetime
from faker import Factory

num = 200

def insert_data():
    faker = Factory.create()
    session = db.session()
    faker_person = [Person(
        SSN = faker.ean8(),
        LastName = faker.first_name(),
        FirstName = faker.last_name(),
        Address = faker.street_address(),
        Telephone = faker.ean8()
        )for i in range(num)]
    session.add_all(faker_person)
    session.commit()
    personSSN = [p.SSN for p in faker_person]
    faker_location = [Location(
        ZipCode = faker.zipcode(),
        City = faker.city(),
        State = faker.state()
        )for i in range(num)]
    session.add_all(faker_location)
    session.commit()
    faker_movie = [Movie(
            Name = faker.name(),
            Type = faker.random_element(elements=('a', 'b', 'c')),
            Rating = faker.pyfloat(left_digits=1, right_digits=1, positive=True),
            NumRating = faker.pyint(),
            ImageUrl = faker.url(),
            Synopsis = faker.sentence(),
            ImdbId = faker.word(),
        )for i in range(num)]
    session.add_all(faker_movie)
    session.commit()
    faker_employee = [Employee(
            SSN = faker.random_element(elements= personSSN),
            StartDate = faker.date(),
            HourlyRate = faker.pyint()
        )for i in range(num)]
    session.add_all(faker_employee)
    session.commit()
    faker_accounts = [Accounts(
            DateOpened = faker.date(),
            Type = faker.random_element(elements=('Limited', 'Unlimited-1', 'Unlimited-2', 'Unlimited-3', 'Admin', 'CustRep')),
            Customer = faker.pyint(),
            UserName = faker.word(),
            PassWord = faker.word()
        )for i in range(num)]
    session.add_all(faker_accounts)
    session.commit()
    for i in range(num):
        cus = Customer(
                Id = personSSN[i],
                Email = faker.email(),
                Rating = faker.pyfloat(left_digits=1, right_digits=1, positive=True),
                CreditCardNumber = faker.credit_card_number() )
        session.add(cus)
        try:
            session.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            session.rollback()
    faker_orders = [Orders(
            OrderDate = faker.date(),
            ReturnDate = faker.date()
        )for i in range(num)]
    session.add_all(faker_orders)
    session.commit()
    faker_actor = [Actor(
            Name = faker.name(),
            Age = faker.pyint(),
            Gender = faker.random_element(elements=('F', 'M', ' ')),
            Rating = faker.pyfloat(left_digits=1, right_digits=1, positive=True),
            NumRating = faker.pyint(),
            ImageUrl = faker.url(),
            Biography = faker.sentence(),
            ImdbId = faker.word()
        )for i in range(num)]
    session.add_all(faker_actor)
    session.commit()
    acc = session.query(Accounts).order_by(Accounts.Id).all()
    cus = session.query(Employee).order_by(Employee.Id).all()
    order = session.query(Orders).order_by(Orders.Id).all()
    movie = session.query(Movie).order_by(Movie.Id).all()
    act = session.query(Actor).order_by(Actor.Id).all()
    accountId = [a.Id for a in acc]
    custRepId = [c.Id for c in cus]
    orderId = [o.Id for o in order]
    movieId = [m.Id for m in movie]
    actorId = [a.Id for a in act]
    faker_rental = [Rental(
            AccountId = faker.random_element(elements=accountId),
            CustRepId = faker.random_element(elements=custRepId),
            OrderId = faker.random_element(elements=orderId),
            MovieId = faker.random_element(elements=movieId),
        )for i in range(num)]
    session.add_all(faker_rental)
    session.commit()
    faker_movieq= [MovieQ(
            AccountId = faker.random_element(elements=accountId),
            MovieId = faker.random_element(elements=movieId),
        )for i in range(num)]
    session.add_all(faker_movieq)
    session.commit()
    faker_movief= [MovieF(
            AccountId = faker.random_element(elements=accountId),
            MovieId = faker.random_element(elements=movieId),
        )for i in range(num)]
    session.add_all(faker_movief)
    session.commit()
    faker_appearedIn = [AppearedIn(
            ActorId = faker.random_element(elements=actorId),
            MovieId = faker.random_element(elements=movieId),
        )for i in range(num)]
    session.add_all(faker_appearedIn)
    session.commit()
    faker_reviews = [Reviews(
            AccountId = faker.random_element(elements=accountId),
            MovieId = faker.random_element(elements=movieId),
            Content = faker.sentence()
        )for i in range(num)]
    session.add_all(faker_reviews)
    session.commit()
if __name__ == '__main__':
    insert_data()
