import csv
from xml.dom.expatbuilder import TEXT_NODE
from dotenv import load_dotenv
import os
from sniffr.app import create_app
from sniffr.models import Activity, Breed, db, Dog, Temperament, User

load_dotenv()

def seed_db_user():
    # Add users
    db.session.add(User(username="jon", email="jon@sniffr.be", password=os.getenv('JON_PASS')))
    db.session.add(User(username="dan", email="dan@sniffr.be", password=os.getenv('DAN_PASS')))
    db.session.add(User(username="josh", email="josh@sniffr.be", password=os.getenv('JOSH_PASS')))
    db.session.add(User(username="allie", email="allie@sniffr.be", password=os.getenv('ALLIE_PASS')))
    db.session.add(User(username="mashima", email="mashima@sniffr.be", password=os.getenv('MASHIMA_PASS')))
    db.session.add(User(username="shaggy", email="shaggyrogers@sniffr.be", password="scooby"))
    db.session.add(User(username="jim", email="jimdavis@sniffr.be", password="odie"))
    db.session.add(User(username="chuck", email="charlesschultz@sniffr.be", password="snoopy"))
    db.session.add(User(username="scott", email="scottadams@sniffr.be", password="dogbert"))
    db.session.add(User(username="walt", email="waltdisney@sniffr.be", password="pluto"))

    db.session.commit()

def seed_db_dog():
    # Add Augie
    db.session.add(Dog(
        dog_name="Augie", 
        age='2',
        owner_id=4,
        breed_id=123,
        sex='Male',
        is_vaccinated=True,
        is_fixed=False
        ))
    db.session.add(Dog(
        dog_name="Scooby Doo", 
        age='2',
        owner_id=6,
        breed_id=123,
        sex='Male',
        is_vaccinated=True,
        is_fixed=False
        ))
    db.session.add(Dog(
        dog_name="Odie", 
        age='35',
        owner_id=7,
        breed_id=123,
        sex='Male',
        is_vaccinated=True,
        is_fixed=True
        ))
    db.session.add(Dog(
        dog_name="Snoopy", 
        age='85',
        owner_id=8,
        breed_id=123,
        sex='Male',
        is_vaccinated=True,
        is_fixed=False
        ))
    db.session.add(Dog(
        dog_name="Dogbert", 
        age='20',
        owner_id=9,
        breed_id=123,
        sex='Male',
        is_vaccinated=True,
        is_fixed=False
        ))
    db.session.add(Dog(
        dog_name="Pluto", 
        age='60',
        owner_id=10,
        breed_id=123,
        sex='Male',
        is_vaccinated=True,
        is_fixed=False
        ))
    db.session.add(Dog(
        dog_name="Pokey", 
        age='10',
        owner_id=2,
        breed_id=123,
        sex='Female',
        is_vaccinated=True,
        is_fixed=True
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
    # Add activities
    db.session.add(Temperament("Shy"))    
    db.session.add(Temperament("Playful"))
    db.session.add(Temperament("Cautious"))
    db.session.add(Temperament("Old and wise"))
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

    #Print Number of Breeds and Breeds List
    print("BREEDS:")
    breeds_result = db.session.query(Breed).all()
    print("There are total of " + str(len(breeds_result)) + " breeds in this database now.")
    # for breed in breeds_result:
    #     print(breed)
    print('-------------------')

        #Print Number of Breeds and Breeds List
    print("TEMPERAMENTS:")
    temperament_result = db.session.query(Temperament).all()
    for row in temperament_result:
        print(row);
    print('-------------------')

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Reset database
        db.drop_all()
        db.create_all()
        
        # Add breeds
        seed_db_breeds()

        # Seed user table
        seed_db_user()

        # Add augie to dog table
        seed_db_dog()

        # Add stuff for the dogs to do.
        seed_db_activities()

        # Add temperament
        seed_db_temperaments()

        # Check results
        check_results()