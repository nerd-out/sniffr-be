from flask import Blueprint, request, make_response, jsonify
from sniffr.models import User, db
import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY")

# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__)

# Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    """When a correct email and password is given, provide a success prompt"""
    content = request.json
    email = content["email"]
    passwd = content["password"]

    # Make sure email and password are provided
    if email and passwd:
        result = db.session.query(User).filter_by(email=f"{email}").first()

        # Check that there is a valid result and a correct password
        if result and result.verify_password(password=passwd):

            # generates the JWT Token
            token = jwt.encode(
                {
                    "user_id": result.user_id,
                    "exp": datetime.utcnow() + timedelta(days=7),
                },
                SECRET_KEY,
            )

            return make_response(jsonify({"token": token}), 201)

        else:
            return {"message": "fail"}, 400

    else:
        return {"message": "fail"}, 400


# Create user route
@auth_bp.route("/createuser", methods=["POST"])
def create_user():
    """Creates a user when a username, password, and email."""

    # Grab json content
    content = request.json
    email = content["email"]
    passwd = content["password"]
    username = content["password"]

    # Create user
    new_user = User(username=username, password=passwd, email=email)
    db.session.add(new_user)
    db.session.commit()

    return {
        "user_id": new_user.user_id,
        "username": new_user.username,
        "email": new_user.email,
    }
