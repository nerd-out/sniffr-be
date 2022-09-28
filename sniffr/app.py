from flask import Flask
import os
from sniffr.auth_routes.auth_routes import auth_bp
from sniffr.activity_routes.activity_routes import activity_bp
from sniffr.breed_routes.breed_routes import breed_bp
from sniffr.dog_routes.dog_routes import dog_bp
from sniffr.temperament_routes.temperament_routes import temperament_bp
from sniffr.size_routes.size_routes import size_bp
from sniffr.user_routes.user_routes import user_bp
from sniffr.swipe_routes.swipe_routes import swipe_bp
from sniffr.match_routes.match_routes import match_bp
from sniffr.models import db, migrate
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(settings_override=None):
    flask_env = os.getenv("DEV_ENV")
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Load app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    CORS(app)

    # settings_override helps with testing
    if settings_override:
        app.config.update(settings_override)

    # Load database given flask_env env variable
    if flask_env == "production":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("PG_DATABSE_URI")
        print("Using prod environment")
    elif flask_env == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DOCKER_DB_URL")
        print("Using test/docker environment")

    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            basedir, "sniffrdb.db"
        )
        print(
            f'Using development set up for \
                SQLALCHEMY_DATABASE_URI: {app.config["SQLALCHEMY_DATABASE_URI"]}'
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Show flask where the tables are

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def home_route():
        return "<h3>Welcome to Sniffr's Backend! Feel free to take a whiff!</h3>"

    # Register Blueprints
    # Auth routes
    app.register_blueprint(auth_bp)

    # Activity routes
    app.register_blueprint(activity_bp)

    # Breed routes
    app.register_blueprint(breed_bp)

    # Dog routes
    app.register_blueprint(dog_bp)

    # Temperament Routes
    app.register_blueprint(temperament_bp)

    # Size Routes
    app.register_blueprint(size_bp)

    # User Routes
    app.register_blueprint(user_bp)

    # Swipe Routes
    app.register_blueprint(swipe_bp)

    # Match Routes
    app.register_blueprint(match_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
