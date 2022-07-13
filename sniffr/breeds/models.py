from sniffr.models import db

class Breed(db.Model):
    __tablename__ = "breeds"

    breed_id = db.Column(db.Integer, primary_key=True)
    breed_name = db.Column(db.Text(), nullable=False)

    def __init__(
        self,
        breed_name      
    ):
        self.breed_name = breed_name

    def __repr__(self):
        return f"<Breed #{self.breed_id} {self.breed_name}>"