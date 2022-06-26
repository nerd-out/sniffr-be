from sqlalchemy import create_engine
from models import Dog, User
import os
from sqlalchemy.orm import sessionmaker

def seed_db_user():
    engine = create_engine('sqlite:///sniffrdb.db')

    Session = sessionmaker(bind = engine)
    session = Session()

    # Add user
    session.add(User(username="jon", email="jon@sniffr.be", password="spice"))
    session.commit()

    # Add user
    session.add(User(username="dan", email="dan@sniffr.be", password="blue"))
    session.commit()

    # Add user
    session.add(User(username="josh", email="josh@sniffr.be", password="apple"))
    session.commit()

    # Add user
    session.add(User(username="allie", email="allie@sniffr.be", password="lalala"))
    session.commit()

    # Add user
    session.add(User(username="mashima", email="mashima@sniffr.be", password="noob"))
    session.commit()

def check_results():
    Session = sessionmaker(bind = engine)
    session = Session()
    result = session.query(User).all()
    for row in result:
        print("Name: ",row.username, "PW:",row.password, "Email:",row.email, "ID:",row.user_id)