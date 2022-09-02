import csv
from xml.dom.expatbuilder import TEXT_NODE
from dotenv import load_dotenv
import os
from sniffr.app import create_app
from sniffr.models import Activity, Breed, db, Dog, Temperament, User, Size

load_dotenv()

def seed_db_user():
    # Add users
    db.session.add(User(username="jon", email="jon@sniffr.be", password=os.getenv('JON_PASS')))
    db.session.add(User(username="dan", email="dan@sniffr.be", password=os.getenv('DAN_PASS')))
    print(os.getenv('DAN_PASS'))
    db.session.add(User(username="josh", email="josh@sniffr.be", password=os.getenv('JOSH_PASS')))
    print(os.getenv('JOSH_PASS'))
    db.session.add(User(username="allie", email="allie@sniffr.be", password=os.getenv('ALLIE_PASS')))
    print(os.getenv('ALLIE_PASS'))
    db.session.add(User(username="mashima", email="mashima@sniffr.be", password=os.getenv('MASHIMA_PASS')))
    print(os.getenv('MASHIMA_PASS'))
    db.session.commit()

def seed_db_dog():
    # Add dogs
    db.session.add(Dog(
        dog_name="Augie", 
        age='2',
        owner_id=4,
        breed_id=123,
        sex='Male',
        is_vaccinated=True,
        is_fixed=False,
        size_id=4,
        temperament_id=2,
        ))
    db.session.add(Dog(
        dog_name="Max", 
        age='15',
        owner_id=4,
        breed_id=137,
        sex='Male',
        is_vaccinated=True,
        is_fixed=False,
        size_id=3,
        temperament_id=2,
        ))
    db.session.add(Dog(
        dog_name="Siri", 
        age='10',
        owner_id=4,
        breed_id=61,
        sex='Female',
        is_vaccinated=True,
        is_fixed=True,
        size_id=5,
        temperament_id=3,
        ))
    db.session.commit()

#Seed database with breeds
def seed_db_breeds():
  with open('./sniffr/data/breeds.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    
    next(spamreader)

    for row in spamreader:
      db.session.add(Breed(breed_name=row[0]))
    
    db.session.commit()

def seed_db_activities():
    # Add activities
    db.session.add(Activity(activity_description="Walking"))    
    db.session.add(Activity(activity_description="Fetching"))
    db.session.add(Activity(activity_description="Frisbee"))
    db.session.add(Activity(activity_description="Sniffing"))
    db.session.add(Activity(activity_description="Chasing Squirrels"))
    db.session.add(Activity(activity_description="Staring at a blank wall"))
    db.session.add(Activity(activity_description="Drinking from the toilet"))
    db.session.commit()

def seed_db_temperaments():
    # Add temperaments
    db.session.add(Temperament("Saucy"))
    db.session.add(Temperament("Playful"))
    db.session.add(Temperament("Cautious"))
    db.session.add(Temperament("Clingy"))
    db.session.add(Temperament("Permanently Ecstatic"))
    db.session.add(Temperament("Old and wise"))
    db.session.commit()

def seed_db_sizes():
    # Add sizes
    db.session.add(Size(size="Teacup (less than 5 lbs)"))    
    db.session.add(Size(size="Toy (6 to 12 lbs)"))    
    db.session.add(Size(size="Small (13 to 24 lbs)"))
    db.session.add(Size(size="Medium (25 to 59 lbs)"))
    db.session.add(Size(size="Large (60 to 99 lbs)"))
    db.session.add(Size(size="Giant (100+ pounds)"))
    db.session.commit()

def check_results():
    """ Prints out the results of the database for users, dogs, and activities """
    print("USERS:")
    result = db.session.query(User).all()
    for row in result:
        print(row)
    print('-------------------')

    print("DOGS:")
    result = db.session.query(Dog).all()
    for row in result:
        print(row)
    print('-------------------')

    print("ACTIVITIES:")
    result = db.session.query(Activity).all()
    for row in result:
        print(row)
    print('-------------------')

    print("BREEDS:")
    result = db.session.query(Breed).all()
    print("There are total of " + str(len(result)) + " breeds in this database now.")
    print('-------------------')

    print("TEMPERAMENTS:")
    result = db.session.query(Temperament).all()
    for row in result:
        print(row);
    print('-------------------')

    print("SIZES:")
    result = db.session.query(Size).all()
    for row in result:
        print(row);
    print('-------------------')

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Reset database
        db.drop_all()
        db.create_all()

        # Add temperament
        seed_db_temperaments()
        
        # Add breeds
        seed_db_breeds()

        # Add Sizes
        seed_db_sizes()

        # Seed user table
        seed_db_user()

        # Add dogs + augie to dog table
        seed_db_dog()

        # Add stuff for the dogs to do
        seed_db_activities()

        # Check results
        check_results()