import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect
import jwt
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.getenv("SECRET_KEY")

# Set up flask & sqlalchemy
db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text(), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.Text())
    birthday = db.Column(db.Date)
    gender = db.Column(db.Text())
    user_pic = db.Column(db.Text())
    user_bio = db.Column(db.Text())
    role = db.Column(db.Text())
    max_distance = db.Column(db.Integer)
    zipcode = db.Column(db.Text())
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now())
    last_update = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"#{self.user_id} {self.email} ({self.role}) | {self.creation_time.strftime('%D %T')} "


class Swipe(db.Model):
    __tablename__ = "swipes"

    swipe_id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey("dogs.dog_id"))
    swiped_dog_id = db.Column(db.Integer, db.ForeignKey("dogs.dog_id"))
    is_interested = db.Column(db.Boolean)
    creation_time = db.Column(db.DateTime)

    def __init__(self, dog_id, swiped_dog_id, is_interested):
        self.dog_id = dog_id
        self.swiped_dog_id = swiped_dog_id
        self.is_interested = is_interested
        self.creation_time = datetime.datetime.now()

    def __repr__(self):
        return f"Dog {self.dog_id} swiped on dog {self.swiped_dog_id} and is {'' if self.is_interested else 'not'} interested in playing."


class Breed(db.Model):
    __tablename__ = "breeds"

    breed_id = db.Column(db.Integer, primary_key=True)
    breed_name = db.Column(db.Text(), nullable=False)

    def __init__(
        self,
        breed_name    
    ):
        self.breed_name = breed_name

    def __repr__(self):
        return f"Breed #{self.breed_id} {self.breed_name}"


class Dog(db.Model):
    __tablename__ = "dogs"

    dog_id = db.Column(db.Integer, primary_key=True)
    dog_name = db.Column(db.Text(), nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    owner = db.relationship("User")

    breed_id = db.Column(db.Integer, db.ForeignKey("breeds.breed_id"), nullable=False)
    breed = db.relationship("Breed")

    size_id = db.Column(db.Integer, db.ForeignKey("sizes.size_id"), nullable=False)
    size = db.relationship("Size")

    temperament_id = db.Column(db.Integer, db.ForeignKey("temperaments.temperament_id"), nullable=False)
    temperament = db.relationship("Temperament", backref=db.backref("dogs"))

    dog_activities = db.relationship("DogActivity", backref=db.backref("dogs"))

    age = db.Column(db.Text(), nullable=False)
    sex = db.Column(db.Text(), nullable=False)
    is_vaccinated = db.Column(db.Boolean, nullable=False)
    is_fixed = db.Column(db.Boolean, nullable=False)
    dog_bio = db.Column(db.Text())
    dog_pic = db.Column(db.Text())
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now())
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f"Dog ({self.dog_id}): {self.dog_name} | Breed: {self.breed.breed_name} | Size: {self.size.size} | Temperament: {self.temperament.temperament_type} | Age: {self.age} | Sex: {self.sex} | Fixed: {self.is_fixed} | Vx: {self.is_vaccinated} | Pic: {self.dog_pic} | Bio: {self.dog_bio} | Created: {self.creation_time:%Y-%m-%d}"


class Size(db.Model):
    __tablename__ = "sizes"

    size_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Text(), nullable=False)

    def __init__(
        self,
        size      
    ):
        self.size = size

    def __repr__(self):
        return f"Size #{self.size_id} {self.size}"


class Temperament(db.Model):
    __tablename__ = "temperaments"

    temperament_id = db.Column(db.Integer, primary_key=True)
    temperament_type = db.Column(db.Text(), nullable=False)

    def __init__(
        self,
        temperament_type
    ):
        self.temperament_type  = temperament_type

    def __repr__(self):
        return f"Temperament ID #{self.temperament_id}: {self.temperament_type}"


class Activity(db.Model):
    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, primary_key=True)
    activity_description = db.Column(db.Text(), nullable=False)


    def __init__(self, activity_description):
        self.activity_description = activity_description
        
    def __repr__(self):
        return f"Description: {self.activity_description}"


class DogActivity(db.Model):
    __tablename__ = "dog_activities"

    dog_activity_id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey("dogs.dog_id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.activity_id"))


    def __init__(
        self,
        dog_id,
        activity_id
    ):
        self.dog_id = dog_id
        self.activity_id = activity_id

    def __repr__(self):
        return f"Dog #{self.dog_id} | Activitity #{self.dog_activity_id}"


class Match(db.Model):
    __tablename__ = "matches"

    match_id = db.Column(db.Integer, primary_key=True)
    dog_id_one = db.Column(db.Integer)
    dog_id_two = db.Column(db.Integer)
    creation_time = db.Column(db.DateTime)

    def __init__(self, dog_id_one, dog_id_two):
        self.dog_id_one = dog_id_one
        self.dog_id_two = dog_id_two
        self.creation_time = datetime.datetime.now()

    def __repr__(self):
        return f"Match # {self.match_id}: Dog {self.dog_id_one} & Dog{self.dog_id_two} on {self.creation_time}"


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


def process_record(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            
        # return 401 if token is not passed
        if not token:
            return {'message' : 'Token is missing'}, 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query\
                .filter_by(user_id = data['user_id'])\
                .first()
        except:
            return {'message' : 'Token is invalid !!'}, 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)

    return decorated

def process_dogs(sqlalchemy_records):
    records = []
    for record in sqlalchemy_records:
        processed_record = record.__dict__

        # Add extra info
        processed_record['breed_name'] = record.breed.breed_name
        processed_record['temperament_type'] = record.temperament.temperament_type
        processed_record['size'] = record.size.size
        processed_record['owner_email'] = record.owner.email
        processed_record['owner_name'] = record.owner.name

        # Remove long annoying text
        del processed_record["_sa_instance_state"]
        del processed_record["breed"]
        del processed_record["temperament"]
        del processed_record['owner']

        records.append(processed_record)
    return records

def process_dog(sqlalchemy_record):
    processed_record = sqlalchemy_record.__dict__

    # Add extra info
    processed_record['breed_name'] = sqlalchemy_record.breed.breed_name
    processed_record['temperament_type'] = sqlalchemy_record.temperament.temperament_type
    processed_record['size'] = sqlalchemy_record.size.size
    processed_record['owner_email'] = sqlalchemy_record.owner.email
    processed_record['owner_name'] = sqlalchemy_record.owner.name

    # Remove long annoying text
    del processed_record["_sa_instance_state"]
    del processed_record["breed"]
    del processed_record["temperament"]
    del processed_record['owner']


    return processed_record


def get_users_dogs_id(user_id):
    queried_dog = (
        db.session.query(Dog)
        .join(User, Dog.owner_id == User.user_id)
        .filter(Dog.owner_id == user_id)
        .first()
    )

    # Return id
    return int(queried_dog.dog_id)
