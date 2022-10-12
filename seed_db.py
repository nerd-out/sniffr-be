import csv
from xml.dom.expatbuilder import TEXT_NODE
from dotenv import load_dotenv
import os
from sniffr.app import create_app
from sniffr.models import (
    Activity,
    Breed,
    db,
    Dog,
    Temperament,
    User,
    Size,
    Swipe,
)
import datetime

load_dotenv()


def seed_db_user():
    """
    This function seeds the datbase with users.
    """

    # Add Jon
    jon = User(email="jon@sniffr.be", password=os.getenv("JON_PASS"))
    jon.name = "Jon"
    jon.birthday = datetime.datetime(2000, 1, 1)
    jon.gender = "Male"
    jon.user_pic = "jon_pic.jpg"
    jon.user_bio = "Sniffr developer"
    jon.role = "Developer"
    jon.max_distance = 5
    jon.zipcode = "00000"
    db.session.add(jon)

    # Add Dan
    dan = User(email="dan@sniffr.be", password=os.getenv("DAN_PASS"))
    dan.name = "Dan"
    dan.birthday = datetime.datetime(2000, 1, 1)
    dan.gender = "Male"
    dan.user_pic = "dan_pic.jpg"
    dan.user_bio = "Sniffr developer"
    dan.role = "Developer"
    dan.max_distance = 5
    dan.zipcode = "00000"
    db.session.add(dan)

    # Add Josh
    josh = User(email="josh@sniffr.be", password=os.getenv("JOSH_PASS"))
    josh.email = "josh@sniffr.be"
    josh.password = os.getenv("JOSH_PASS")
    josh.name = "Josh"
    josh.birthday = datetime.datetime(2000, 1, 1)
    josh.gender = "Male"
    josh.user_pic = "josh_pic.jpg"
    josh.user_bio = "Sniffr developer"
    josh.role = "Developer"
    josh.max_distance = 5
    josh.zipcode = "00000"
    db.session.add(josh)

    # Add Allie
    allie = User(email="allie@sniffr.be", password=os.getenv("ALLIE_PASS"))
    allie.name = "Allie"
    allie.birthday = datetime.datetime(2000, 1, 1)
    allie.gender = "Female"
    allie.user_pic = "allie_pic.jpg"
    allie.user_bio = "Sniffr developer"
    allie.role = "Developer"
    allie.max_distance = 5
    allie.zipcode = "00000"
    db.session.add(allie)

    # Add Mashima
    mashima = User(email="mashima@sniffr.be", password=os.getenv("MASHIMA_PASS"))
    mashima.name = "Mashima"
    mashima.birthday = datetime.datetime(2000, 1, 1)
    mashima.gender = "Female"
    mashima.user_pic = "mashime_pic.jpg"
    mashima.user_bio = "Sniffr developer"
    mashima.role = "Developer"
    mashima.max_distance = 5
    mashima.zipcode = "00000"
    db.session.add(mashima)

    # Add Benedict
    benedict = User(email="benedict@sniffr.be", password=os.getenv("BENEDICT_PASS"))
    benedict.name = "Benedict"
    benedict.birthday = datetime.datetime(2000, 1, 1)
    benedict.gender = "Male"
    benedict.user_pic = "benedict_pic.jpg"
    benedict.user_bio = "Sniffr developer"
    benedict.role = "Developer"
    benedict.max_distance = 5
    benedict.zipcode = "00000"
    db.session.add(benedict)

    # Add Demo
    demo = User(email="demo@sniffr.be", password=os.getenv("DEMO_USER_PASS"))
    demo.name = "Demo"
    demo.birthday = datetime.datetime(2000, 1, 1)
    demo.gender = "Demo"
    demo.user_pic = "demo_pic.jpg"
    demo.user_bio = "Sniffr Demo"
    demo.role = "Demo"
    demo.max_distance = 5
    demo.zipcode = "00000"
    db.session.add(demo)

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
            age="5",
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
            age="8",
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
            age="1000",
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
    db.session.add(
        Dog(
            dog_name="Slink",
            age="17",
            owner_id=2,
            breed_id=153,
            sex="Male",
            is_vaccinated=True,
            is_fixed=True,
            size_id=1,
            temperament_id=2,
            dog_bio="Now Slinky here is as loyal as any dog you could want.",
        )
    )
    db.session.add(
        Dog(
            dog_name="Astro",
            age="6",
            owner_id=6,
            breed_id=7,
            sex="Male",
            is_vaccinated=True,
            is_fixed=True,
            size_id=5,
            temperament_id=3,
            dog_bio="Elroy Jeston found a dog and brought him home, even though his father George Jetson is against having a dog - Episode aired Oct 21, 1962.",
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
    db.session.add(Activity(activity_description="Swimming"))
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
