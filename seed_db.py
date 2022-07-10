from sniffr.models import Dog, User, Activity, db
import os
from sniffr.app import create_app
from dotenv import load_dotenv

load_dotenv()

def seed_db_user():

    # Add user
    db.session.add(User(username="jon", email="jon@sniffr.be", password=os.getenv('JON_PASS')))
    # Add user
    db.session.add(User(username="dan", email="dan@sniffr.be", password=os.getenv('DAN_PASS')))
    # Add user
    db.session.add(User(username="josh", email="josh@sniffr.be", password=os.getenv('JOSH_PASS')))
    # Add user
    db.session.add(User(username="allie", email="allie@sniffr.be", password=os.getenv('ALLIE_PASS')))
    # Add user
    db.session.add(User(username="mashima", email="mashima@sniffr.be", password=os.getenv('MASHIMA_PASS')))
    db.session.commit()

def seed_db_dog():

    # Add Augie
    db.session.add(Dog(
        dog_name="Augie", 
        age=2,
        user_id=4,
        sex='Male'))
    db.session.commit()

def check_results():
    """ Prints out the results of the database for users, dogs, and activities """
    result = db.session.query(User).all()
    for row in result:
        print(
            "Name: ",
            row.username,
            "PW:",
            row.password,
            "Email:",
            row.email,
            "ID:",
            row.user_id,
        )

    result = db.session.query(Dog).all()
    for row in result:
        print(
            "# ",
            row.dog_id,
            "Dog:",
            row.dog_name,
            "Age:",
            row.age,
            "Sex:",
            row.sex,
            "Owner:",
            row.user_id,
        )

    result = db.session.query(Activity).all()
    for row in result:
        print(
            "# ",
            row.activity_id,
            "Activity:",
            row.activity_description,
        )

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


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Reset database
        db.drop_all()
        db.create_all()

        # Seed user table
        seed_db_user()

        # Add augie to dog table
        seed_db_dog()

        # Add stuff for the dogs to do.
        seed_db_activities()

        # Check results
        check_results()