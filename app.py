from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def our_first_route():
    return "<h3>Welcome to Sniffr's Backend! Feel free to take a whiff!</h3>"


if __name__ == "__main__":
    app.run()
