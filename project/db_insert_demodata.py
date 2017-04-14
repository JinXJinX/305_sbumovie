from app import db
from app.models import *
from datetime import datetime
from faker import Factory

num = 200

def insert_data():
    faker = Factory.create()
    session = db.session()

    faker_location = [Location(
        ZipCode = faker.zipcode(),
        City = faker.city(),
        State = faker.state()
        )for i in range(num)]
    for l in faker_location:
        try:
            session.add(l)
            session.commit()
        except:
            session.rollback()

    loc = [l.ZipCode for l in faker_location]

    faker_accounts = [Accounts(
            Id = faker.pyint(),
            DateOpened = faker.date(),
            Type = faker.random_element(elements=('Limited', 'Unlimited-1', 'Unlimited-2', 'Unlimited-3', 'Admin', 'CustRep')),
            UserName = faker.word(),
            PassWord = faker.word(),
            LastName = faker.first_name(),
            FirstName = faker.last_name(),
            Address = faker.street_address(),
            ZipCode = faker.random_element(elements=loc),
            Phone = faker.ean8(),
            Email = faker.email(),
            Rating = faker.pyfloat(left_digits=1, right_digits=1, positive=True),
            CreditCardNumber = faker.ean8()
        )for i in range(num)]
    for f in faker_accounts:
        try:
            session.add(f)
            session.commit()
        except:
            session.rollback()

    accId = [a.Id for a in faker_accounts]

    faker_movie = [Movie(
            Id = faker.pyint(),
            Name = faker.name(),
            Type = faker.random_element(elements=('a', 'b', 'c')),
            Rating = faker.pyfloat(left_digits=1, right_digits=1, positive=True),
            NumRating = faker.pyint(),
            ImageUrl = faker.url(),
            Synopsis = faker.sentence(),
            ImdbId = faker.word(),
        )for i in range(num)]
    for m in faker_movie:
        try:
            session.add(m)
            session.commit()
        except:
            session.rollback()

    movId = [m.Id for m in faker_movie]

    faker_employee = [Employee(
            Id = faker.pyint(),
            SSN = faker.ean8(),
            StartDate = faker.date(),
            HourlyRate = faker.pyint(),
            AccountId = faker.random_element(elements= accId)
        )for i in range(num)]
    for e in faker_employee:
        try:
            session.add(e)
            session.commit()
        except:
            session.rollback()

    empId = [e.Id for e in faker_employee]

    faker_orders = [Orders(
            OrderDate = faker.date(),
            ReturnDate = faker.date(),
            AccountId = faker.random_element(elements= accId),
            CustRepId = faker.random_element(elements= empId),
            MovieId = faker.random_element(elements= movId),
            Price = faker.pyfloat(left_digits=4, right_digits=2, positive=True),
        )for i in range(num)]
    session.add_all(faker_orders)
    session.commit()

    faker_actor = [Actor(
            Id = faker.pyint(),
            Name = faker.name(),
            Age = faker.pyint(),
            Gender = faker.random_element(elements=('F', 'M', ' ')),
            Rating = faker.pyfloat(left_digits=1, right_digits=1, positive=True),
            NumRating = faker.pyint(),
            ImageUrl = faker.url(),
            Biography = faker.sentence(),
            ImdbId = faker.word()
        )for i in range(num)]
    for a in faker_actor:
        try:
            session.add(a)
            session.commit()
        except:
            session.rollback()

    actId = [a.Id for a in faker_actor]

    faker_movieq= [MovieQ(
            AccountId = faker.random_element(elements=accId),
            MovieId = faker.random_element(elements=movId),
        )for i in range(num)]
    session.add_all(faker_movieq)
    session.commit()

    faker_movief= [MovieF(
            AccountId = faker.random_element(elements=accId),
            MovieId = faker.random_element(elements=movId),
        )for i in range(num)]
    session.add_all(faker_movief)
    session.commit()

    faker_appearedIn = [AppearedIn(
            ActorId = faker.random_element(elements=actId),
            MovieId = faker.random_element(elements=movId),
        )for i in range(num)]
    session.add_all(faker_appearedIn)
    session.commit()

    faker_reviews = [Reviews(
            AccountId = faker.random_element(elements=accId),
            MovieId = faker.random_element(elements=movId),
            Content = faker.sentence(),
            Title = faker.word()
        )for i in range(num)]
    session.add_all(faker_reviews)
    session.commit()
if __name__ == '__main__':
    insert_data()
