from app import db

from app.models import Person
from datetime import datetime
from sqlalchemy import create_engine, Table, MetaData, UniqueConstraint
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from faker import Factory

def insert_data():
    faker = Factory.create()
    Session = sessionmaker(bind=engine)
    session = Session()
    faker_person = [Person(
        SSN = faker.ssn(),
        LastName = faker.name(),
        FirstName = faker.name(),
        Address = faker.address(),
        Telephone = faker.phone_number() )]
    session.add_all(faker_person)
    session.commit()

if __name__ == '__main__':
    insert_data()
