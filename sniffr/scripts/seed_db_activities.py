from sqlalchemy import create_engine
from models import Activity
import os
from sqlalchemy.orm import sessionmaker

def seed_db_activities():
    engine = create_engine('sqlite:///sniffrdb.db')

    Session = sessionmaker(bind = engine)
    session = Session()

    # Add activity
    session.add(Activity(activity_description="Walking"))
    session.commit()

    # Add activity
    session.add(Activity(activity_description="Fetching"))
    session.commit()

    # Add activity
    session.add(Activity(activity_description="Frisbee"))
    session.commit()

    # Add activity
    session.add(Activity(activity_description="Sniffing"))
    session.commit()

    # Add activity
    session.add(Activity(activity_description="Chasing Squirrels"))
    session.commit()

    # Add activity
    session.add(Activity(activity_description="Staring at a blank wall"))

    # Add activity
    session.add(Activity(activity_description="Drinking from the toilet"))
    session.commit()
    
def check_results():
    Session = sessionmaker(bind = engine)
    session = Session()
    result = session.query(Activity).all()
    for row in result:
        print("Activity: ", row.activity_description)
