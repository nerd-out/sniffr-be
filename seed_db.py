from sniffr.models import Dog, User, db
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

        # Check results
        check_results()