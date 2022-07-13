import csv
from sniffr.breeds.models import Breed, db

def seed_db_breeds():
  with open('./sniffr/breeds/breeds.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    
    next(spamreader)

    for row in spamreader:
      db.session.add(Breed(breed_name=row[0]))
    
    db.session.commit()