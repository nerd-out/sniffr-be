from flask import Flask, jsonify
from dotenv import load_dotenv
import os

# from sniffr.models import db, migrate, Dog

load_dotenv()


def create_app():

    app = Flask(__name__)

    # # PostGres Connection
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("PG_DATABASE_URL")
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # # Show flask where the tables are
    # db.init_app(app)
    # migrate.init_app(app, db)

    @app.route("/")
    def our_first_route():
        return "<h3>Welcome to Sniffr's Backend! Feel free to take a whiff!</h3>"

    # @app.route("/all_dogs")
    # def all_dogs():
    #     dogs = Dog.query.all()
    #     return f"{dogs}"

    # @app.route("/add_dog/<dog_name>/<dog_age>")
    # def add_dog(dog_name, dog_age):
    #     dog = Dog(dog_name=dog_name, dog_age=dog_age)
    #     db.session.add(dog)
    #     db.session.commit()

    #     # Return the dog that was just added
    #     dog_id = db.session.query(Dog).get(dog.dog_id)

    #     return jsonify({"DogID": f"{dog_id}"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
