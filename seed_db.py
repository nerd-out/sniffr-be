import csv
from xml.dom.expatbuilder import TEXT_NODE
from dotenv import load_dotenv
import os
from sniffr.app import create_app
from sniffr.models import Activity, Breed, db, Dog, Temperament, User, Size, DogActivity, Swipe

load_dotenv()


def seed_db_user():
    """
    This function seeds the datbase with users.
    """
    db.session.add(User(email="jon@sniffr.be", password=os.getenv("JON_PASS")))
    db.session.add(User(email="dan@sniffr.be", password=os.getenv("DAN_PASS")))
    db.session.add(User(email="josh@sniffr.be", password=os.getenv("JOSH_PASS")))
    db.session.add(User(email="allie@sniffr.be", password=os.getenv("ALLIE_PASS")))
    db.session.add(User(email="mashima@sniffr.be", password=os.getenv("MASHIMA_PASS")))
    db.session.add(
        User(email="benedict@sniffr.be", password=os.getenv("BENEDICT_PASS"))
    )
    db.session.add(User(email="demo@sniffr.be", password=os.getenv("DEMO_USER_PASS")))
    db.session.commit()


def seed_db_dog():
    """
    This function seeds the datbase with dogs.
    """
    db.session.add(
        Dog(
            dog_name="Augie",
            age="2",
            owner_id=4,
            breed_id=123,
            sex="Male",
            is_vaccinated=True,
            is_fixed=False,
            size_id=4,
            temperament_id=2,
            dog_bio="A poof of a dog who enjoys playing fetch.",
        )
    )
    db.session.add(
        Dog(
            dog_name="Max",
            age="15",
            owner_id=3,
            breed_id=137,
            sex="Male",
            is_vaccinated=True,
            is_fixed=False,
            size_id=3,
            temperament_id=2,
            dog_bio="Max loves running around the yard, playing chase with other dogs, and finding the local vermin. He's not too good at fetch, but he'll always want to be your friend!",
        )
    )
    db.session.add(
        Dog(
            dog_name="Siri",
            age="10",
            owner_id=1,
            breed_id=61,
            sex="Female",
            is_vaccinated=True,
            is_fixed=True,
            size_id=5,
            temperament_id=3,
            dog_bio="A former frisbee dog who loves playing in the back yard or going swimming!",
        )
    )
    db.session.add(
        Dog(
            dog_name="Cerberus",
            age="10",
            owner_id=7,
            breed_id=151,
            sex="Demon",
            is_vaccinated=False,
            is_fixed=False,
            size_id=6,
            temperament_id=1,
            dog_bio="Cerberus, often referred to as the hound of Hades, is a multi-headed dog that guards the gates of the Underworld to prevent the dead from leaving.",
        )
    )
    db.session.commit()


def seed_db_breeds():
    """
    This function seeds the datbase with breeds.
    """
    with open("./sniffr/data/breeds.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")

        next(spamreader)

        for row in spamreader:
            db.session.add(Breed(breed_name=row[0]))

        db.session.commit()


def seed_db_activities():
    """
    This function seeds the datbase with activities.
    """
    db.session.add(Activity(activity_description="Walks"))
    db.session.add(Activity(activity_description="Fetch"))
    db.session.add(Activity(activity_description="Tricks"))
    db.session.add(Activity(activity_description="Agility"))
    db.session.add(Activity(activity_description="Hikes"))
    db.session.add(Activity(activity_description="Car Rides"))
    db.session.add(Activity(activity_description="Frisbee"))
    db.session.add(Activity(activity_description="Dog Parks"))
    db.session.add(Activity(activity_description="Cuddles"))
    db.session.commit()


def seed_db_temperaments():
    """
    This function seeds the datbase with temperaments.
    """
    db.session.add(Temperament("Saucy"))
    db.session.add(Temperament("Playful"))
    db.session.add(Temperament("Cautious"))
    db.session.add(Temperament("Clingy"))
    db.session.add(Temperament("Permanently Ecstatic"))
    db.session.add(Temperament("Old and wise"))
    db.session.commit()


def seed_db_sizes():
    """
    This function seeds the datbase with dog sizes.
    """
    db.session.add(Size(size="Teacup (less than 5 lbs)"))
    db.session.add(Size(size="Toy (6 to 12 lbs)"))
    db.session.add(Size(size="Small (13 to 24 lbs)"))
    db.session.add(Size(size="Medium (25 to 59 lbs)"))
    db.session.add(Size(size="Large (60 to 99 lbs)"))
    db.session.add(Size(size="Giant (100+ pounds)"))
    db.session.commit()


def seed_db_swipes():
    """
    This function seeds the datbase with swipes.
    """
    # Add swipes

    # Siri doesn't like Augie
    db.session.add(Swipe(dog_id=3, swiped_dog_id=1, is_interested=False))

    # Augie likes Cerberus
    db.session.add(Swipe(dog_id=1, swiped_dog_id=4, is_interested=True))

    db.session.commit()


def check_results():
    """
    Prints out the results of the database
    """
    print("USERS:")
    result = db.session.query(User).all()
    for row in result:
        print(row)
    print("-------------------")

    print("DOGS:")
    result = db.session.query(Dog).all()
    for row in result:
        print(row)
    print("-------------------")

    print("ACTIVITIES:")
    result = db.session.query(Activity).all()
    for row in result:
        print(row)
    print("-------------------")

    print("BREEDS:")
    result = db.session.query(Breed).all()
    print("There are total of " + str(len(result)) + " breeds in this database now.")
    print("-------------------")

    print("TEMPERAMENTS:")
    result = db.session.query(Temperament).all()
    for row in result:
        print(row)
    print("-------------------")

    print("SIZES:")
    result = db.session.query(Size).all()
    for row in result:
        print(row)
    print("-------------------")

    print("SWIPES:")
    result = db.session.query(Swipe).all()
    for row in result:
        print(row)
    print("-------------------")


def seed_db():
    """
    A function that seeds the database by:
        dropping everything,
        creating the tables,
        and then seeding each table
    """
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

    # Add swipes
    seed_db_swipes()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_db()

        # Check results
        check_results()
