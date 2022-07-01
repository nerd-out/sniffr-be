import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Set up flask & sqlalchemy
db = SQLAlchemy()
migrate = Migrate()



class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), unique=True)
    email = db.Column(db.Text(), unique=True)
    password = db.Column(db.Text(), unique=True)
    created_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    dog = db.relationship("Dog", backref="owner", lazy="dynamic")

    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.created_on = datetime.datetime.now()
        self.admin = admin

    def __repr__(self):
        return "<User {}>".format(self.username)


# Let's create the dog table
class Dog(db.Model):
    __tablename__ = "dogs"

    dog_id = db.Column(db.Integer, primary_key=True)
    dog_name = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # breed_id = db.Column(db.Integer, nullable=False)
    # size_id = db.Column(db.Integer, nullable=False)
    # temperament_id = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.Text(), nullable=False)
    # is_vaccinated = db.Column(db.Boolean, nullable=False)
    # is_fixed = db.Column(db.Boolean, nullable=False)
    # dog_bio = db.Column(db.Text(), nullable=False)
    # dog_pic = db.Column(db.Text(), nullable=False)
    creation_time = db.Column(db.DateTime)
    # last_update = db.Column(db.DateTime)

    def __init__(
        self,
        dog_name,
        user_id,
        age,
        sex,
    ):
        self.dog_name = dog_name
        self.user_id = user_id
        self.age = age
        self.sex = sex
        self.creation_time = datetime.datetime.now()

    def __repr__(self):
        return f"<Dog: {self.dog_name} | Age: {self.age}>"



def process_records(sqlalchemy_records):
    """
    A helper method for converting a list of database record objects into a list of dictionaries, so they can be returned as JSON
    Param: database_records (a list of db.Model instances)
    Example: parse_records(User.query.all())
    Returns: a list of dictionaries
    """
    records = []
    for record in sqlalchemy_records:
        processed_record = record.__dict__
        del processed_record["_sa_instance_state"]
        processed_record.update({'Success': True})
        records.append(processed_record)
    return records

