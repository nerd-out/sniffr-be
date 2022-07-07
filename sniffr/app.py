from flask import Flask # , jsonify
from sniffr.auth_routes.views import auth_bp
from sniffr.dog_routes.dog_routes import dog_bp
from sniffr.activity_routes.activity_routes import activity_bp
from dotenv import load_dotenv
# from flask_cors import cross_origin

import os

load_dotenv()

import sys

from sniffr.models import db, migrate # , Dog, process_records

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    flask_env = os.getenv("FLASK_ENV")
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Load app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY


    # Load database given flask_env env variable
    if flask_env == "production":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("PG_DATABSE_URI")
        print("Using prod environment")

    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            basedir, "sniffrdb.db"
        )
        print(
            f'Using development set up for SQLALCHEMY_DATABASE_URI: {app.config["SQLALCHEMY_DATABASE_URI"]}'
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Show flask where the tables are
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def our_first_route():
        return "<h3>Welcome to Sniffr's Backend! Feel free to take a whiff!</h3>"

    # @app.route("/all_dogs")
    # @cross_origin()
    # def all_dogs():
    #     dogs = Dog.query.all()
    #     dogs = process_records(dogs)
    #     return jsonify(dogs)

    # @app.route("/add_dog/<dog_name>/<dog_age>")
    # def add_dog(dog_name, dog_age):
    #     dog = Dog(dog_name=dog_name, dog_age=dog_age)
    #     db.session.add(dog)
    #     db.session.commit()

    #     # Return the dog that was just added
    #     dog_id = db.session.query(Dog).get(dog.dog_id)

    #     return jsonify({"DogID": f"{dog_id}"})


    with app.app_context():

        # Register Blueprints

        # Auth routes
        app.register_blueprint(auth_bp)

        # Dog routes
        app.register_blueprint(dog_bp)

        # Activity routes
        app.register_blueprint(activity_bp)

        return app



if __name__ == "__main__":
    app = create_app()
    app.run()
