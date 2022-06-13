from flask import Flask, jsonify
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():

    app = Flask(__name__)

    # PostGres Connection
    

    @app.route("/")
    def our_first_route():
        return "<h3>Welcome to Sniffr's Backend! Feel free to take a whiff!</h3>"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
