class MovieType(Enum):
    COMEDY = 1
    DRAMA = 2
    ACTION = 3
    FOREIGN = 4
    NA = 5  #defualt value

class AccountType(Enum):
    L1 = 'Limited'
    L2 = 'unlimited-1'
    L3 = 'unlimited-2'
    L4 = 'unlimited-3'

class EmployeeType(Enum):
    EMPLOYEE = 'Employee'
    EMPLOYER = 'Employer'

class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum(MovieType))
    fee = db.Column(db.DECIMAL(8,2), nullable=False)
    copies = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer)

class Actor(db.Model):
    __tablename__ = 'Actor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actor_name = db.Column(db.String(50), nullable=False)
    actor_sex = db.Column(db.String(10))
    actor_age = db.Column(db.Integer)
    rating = db.Column(db.Integer)

class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False, unique=True) #this is login id
    last_name = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    address = db.Column(db.String(50))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zipcode = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum(AccountType), nullable=False, default=AccountType.L1)
    creation_data = db.Column(db.Date, nullable=False)
    card_num = db.Column(db.String(20))
    rating = db.Column(db.Integer)


class Employee(db.Model):
    __tablename__ = 'Employee'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ssn = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    hourly_rating = db.Column(db.DECIMAL(8,2), nullable=False)
    type = db.Column(db.Enum(EmployeeType), nullable=False)

class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    movie_id = db.relationship('Movie', backref='id')
    customer_id = db.relationship('Customer', backref='id')
    employee_id = db.relationship('Employee', backref='id')
'''
class Perform(db.Model):
    __tablename__ = 'Perform'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actor_id = db.relationship('Actor', backref='id')
    movie_id = db.relationship('Movie', backref='id')

class Queue(db.Model):
    __tablename__ = 'Queue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.relationship('Customer', backref='id')
    movie_id = db.relationship('Movie', backref='id')

class History(db.Model):
    __tablename__ = 'History'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.relationship('Customer', backref='id')
    order_id = db.relationship('Order', backref='id')
'''


Perform = Table(
    'Perform', Base.metadata,
    Column('actor_id', Integer, ForeignKey('Actor.id')),
    Column('movie_id', Integer, ForeignKey('Movie.id')),
)
Queue = Table(
    'Queue', Base.metadata,
    Column('customer_id', Integer, ForeignKey('Customer.id')),
    Column('movie_id', Integer, ForeignKey('Movie.id')),
)
History = Table(
    'History', Base.metadata,
    Column('customer_id', Integer, ForeignKey('Customer.id')),
    Column('order_id', Integer, ForeignKey('Order.id')),
)
