from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Set up flask & sqlalchemy
db = SQLAlchemy()
migrate = Migrate()


# Tables (models)
# Users
# # User_ID, Password, Picture, Email, First Name, Last Name, Phone, Address, City, State, Zip, Country
# Dogs
# # Dog_ID, Name, Breed, Age, Vaccinated, Description, Picture, Personality, Owner(User)
# Swipes
# # Swipe_ID, Has_swiped, Swipee(Dog), Swiper(Dog)
# Matches
# # Match_ID, Swipee(Dog), Swiper(Dog)

# Let's create the dog table
class Dog(db.Model):
    __tablename__ = "dogs"

    # First column: dog id
    dog_id = db.Column(db.Integer, primary_key=True)

    # Second column: dog name
    dog_name = db.Column(db.Text(), nullable=False)

    # Third column: dog age
    dog_age = db.Column(db.Integer, nullable=False)

    def __init__(self, dog_name, dog_age):
        self.dog_name = dog_name
        self.dog_age = dog_age

    def __repr__(self):
        return f"<Dog: {self.dog_name} | Age: {self.dog_age}>"


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