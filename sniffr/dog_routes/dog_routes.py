from concurrent.futures import process
from datetime import datetime
from lib2to3.pgen2 import token
from flask import Blueprint, request, jsonify, make_response
from sniffr.models import Activity, Dog, db, User, Breed, token_required, process_dogs, process_dog, DogActivity
import os

SECRET_KEY = os.getenv("SECRET_KEY")

# Blueprint Configuration
dog_bp = Blueprint("dog_bp", __name__)

# Get a dog's info


@dog_bp.route("/dog/<dog_id>", methods=["GET"])
def get_dog(dog_id):
    """Get dog info"""
    queried_dog = db.session.query(Dog).join(User).filter(Dog.dog_id == dog_id).first()
    if queried_dog:
        response = process_dog(queried_dog)

        return response

    else:
        response = {}
        return jsonify(response)


# Get All Dogs


@dog_bp.route("/dogs", methods=["GET"])
def get_dogs():

    queried_dogs = (
        db.session.query(Dog)
        .join(User, Dog.owner_id == User.user_id)
        .all()
    )

    if queried_dogs:
        response = process_dogs(queried_dogs)
        return jsonify(response)

    else:
        response = []
        return jsonify(response)


# Get a User's Dogs


@dog_bp.route("/dogs/user", methods=["GET"])
@token_required
def get_users_dogs(current_user):
    """
    Given a jwt, returns a json of that users dogs.
    """

    # Query and get dogs given a user id
    user_id = current_user.user_id
    queried_dog = (
        db.session.query(Dog)
        .join(User, Dog.owner_id == User.user_id)
        .filter(Dog.owner_id == user_id)
        .first()
    )

    # Return response
    response = {}
    if queried_dog:
        response = process_dog(queried_dog)
        return jsonify(response)

    else:
        return jsonify(response), 200


# Create / Edit Dog


@dog_bp.route("/dog", methods=["POST"])
@token_required
def post_dog(current_user):
    """Create or edit dog info"""
    content = request.json
    user_id = int(current_user.user_id)
    
    # If dog_id not in body then they are trying to create
    # If dog_id in body then updating content
    if "dog_id" in content.keys():
        queried_dog = (
            db.session.query(Dog)
            .filter(Dog.dog_id == int(content["dog_id"]))
            .filter(Dog.owner_id == user_id)
            .first()
        )

        if queried_dog:
            # Update properties
            queried_dog.dog_name = content["dog_name"]
            queried_dog.breed_id = content["breed_id"]
            queried_dog.temperament_id = content["temperament_id"]
            queried_dog.size_id = content["size_id"]
            queried_dog.is_vaccinated = content["is_vaccinated"]
            queried_dog.is_fixed = content["is_fixed"]
            queried_dog.age = content["age"]
            queried_dog.sex = content["sex"]
            queried_dog.dog_bio = content["dog_bio"]
            queried_dog.dog_pic = content["dog_pic"]
            queried_dog.last_updated = datetime.now()

            db.session.commit()

            # TODO: Add dog's activities
            

            response = process_dog(queried_dog)

            return jsonify(response)

        else:
            return jsonify({}), 200

    else:
        # create dog

        new_dog = Dog(
            dog_name=content["dog_name"],
            owner_id=user_id,
            breed_id=content["breed_id"],
            size_id=content["size_id"],
            temperament_id=content["temperament_id"],
            age=content["age"],
            sex=content["sex"],
            is_vaccinated=content["is_vaccinated"],
            is_fixed=content["is_fixed"],
            dog_bio=content["dog_bio"],
            dog_pic=content["dog_pic"],
        )

        db.session.add(new_dog)
        db.session.commit()

        # TODO: Add dog's activities
        for activity_id in content['activities']:
            dogs_activity = DogActivity(dog_id=new_dog.dog_id, activity_id=activity_id)
            db.session.add(dogs_activity)
            db.session.commit()

        queried_dog = (
            db.session.query(Dog)
            .join(Breed)
            .join(User)
            .join(DogActivity)
            .join(Activity)
            .filter(Dog.dog_id == new_dog.dog_id)
            .first()
        )
        
        response = process_dog(queried_dog)

        return jsonify(response), 201


# Delete Dog


@dog_bp.route("/dog/<dog_id>", methods=["DELETE"])
@token_required
def delete_dog(current_user, dog_id):
    """Create or edit dog info"""
    user_id = int(current_user.user_id)
    dog_id = int(dog_id)

    queried_dog = db.session.query(Dog).filter(Dog.owner_id==user_id).first()
    
    if queried_dog:
        if queried_dog.owner_id == user_id:
            db.session.delete(queried_dog)
            db.session.commit()

            return jsonify({}), 200

    else:
        return jsonify({}), 204
