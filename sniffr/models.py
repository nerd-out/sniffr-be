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

class Swipe(db.Model):
    __tablename__ = "swipes"

    swipe_id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey("dogs.dog_id"))
    swiped_dog_id = db.Column(db.Integer, db.ForeignKey("dogs.dog_id"))
    is_interested = db.Column(db.Boolean)
    creation_time = db.Column(db.DateTime)

    def __init__(self, swipe_id, dog_id, swiped_dog_id, is_interested):
        self.swipe_id = swipe_id
        self.dog_id = dog_id
        self.swiped_dog_id = swiped_dog_id
        self.is_interested = is_interested
        self.creation_time = datetime.datetime.now()

    def __repr__(self):
        return f"<Dog {self.dog_id} swiped on dog {self.swiped_dog_id} and is {'' if self.is_interested else 'not'} interested in playing.>"


# Let's create the dog table
class Dog(db.Model):
    __tablename__ = "dogs"

    dog_id = db.Column(db.Integer, primary_key=True)
    dog_name = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.Text(), nullable=False)
    creation_time = db.Column(db.DateTime)

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

class Activity(db.Model):
    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, primary_key=True)
    activity_description = db.Column(db.Text(), nullable=False)

    def __init__(self, activity_description):
        self.activity_description = activity_description
        
    def __repr__(self):
        return f"<Description: {self.activity_description}>"

class DogActivity(db.Model):
    __tablename__ = "dog_activities"

    dog_activity_id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey("dogs.dog_id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.activity_id"))
    activity_rank = db.Column(db.Integer(), nullable=False)

    def __init__(
        self,
        dog_id,
        activity_id,
        activity_rank        
    ):
        self.dog_id = dog_id
        self.activity_id = activity_id
        self.activity_rank = activity_rank

    def __repr__(self):
        return f"<Dog {self.dog_id}'s #{self.activity_rank} preference is activity #{self.activity_id}>"


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
        records.append(processed_record)
    return records

