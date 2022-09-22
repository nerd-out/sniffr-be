from concurrent.futures import process
from datetime import datetime
from lib2to3.pgen2 import token
from flask import Blueprint, request, jsonify
from sniffr.models import Dog, db, User, process_record, Breed, token_required
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
        response = process_record(queried_dog)
        response["breed"] = queried_dog.breed.breed_name
        response["size"] = queried_dog.size.size
        response["temperament_type"] = queried_dog.temperament.temperament_type

        return response

    else:
        response = {"message": "Dog Not Found"}
        return response, 404


# Get All Dogs


@dog_bp.route("/dogs", methods=["GET"])
def get_dogs():

    queried_dogs = db.session.query(Dog).join(User, Dog.owner_id == User.user_id).all()
    response = []
    if queried_dogs:
        for row in queried_dogs:
            dog = {
                "owner_id": row.owner.user_id,
                "dog_id": row.dog_id,
                "dog_name": row.dog_name,
                "age": row.age,
                "sex": row.sex,
                "is_vaccinated": row.is_vaccinated,
                "is_fixed": row.is_fixed,
                "dog_bio": row.dog_bio,
                "dog_pic": row.dog_bio,
                "creation_time": row.creation_time,
                "last_updated": row.last_updated,
                "breed_id": row.breed.breed_id,
                "breed": row.breed.breed_name,
                "temperament_id": row.temperament.temperament_id,
                "temperament_type": row.temperament.temperament_type,
                "size_id": row.size.size_id,
                "size": row.size.size,
            }

            response.append(dog)

        return jsonify(response)

    else:
        response = {"message": "Dog Not Found"}
        return response, 404


# Get a User's Dogs


@dog_bp.route("/dogs/user", methods=["GET"])
@token_required
def get_users_dogs(current_user):
    """
    Given a jwt, returns a json of that users dogs.
    """

    # Query and get dogs given a user id
    user_id = current_user.user_id
    queried_dogs = (
        db.session.query(Dog)
        .join(User, Dog.owner_id == User.user_id)
        .filter(Dog.owner_id == user_id)
        .all()
    )

    # Return response
    response = []
    if queried_dogs:
        for row in queried_dogs:
            dog = {
                "owner_id": row.owner.user_id,
                "dog_id": row.dog_id,
                "dog_size": row.size_id,
                "dog_name": row.dog_name,
                "age": row.age,
                "sex": row.sex,
                "is_vaccinated": row.is_vaccinated,
                "is_fixed": row.is_fixed,
                "dog_bio": row.dog_bio,
                "dog_pic": row.dog_bio,
                "creation_time": row.creation_time,
                "last_updated": row.last_updated,
                "breed_id": row.breed.breed_id,
                "breed": row.breed.breed_name,
                "temperament_id": row.temperament.temperament_id,
                "temperament_type": row.temperament.temperament_type,
                "size_id": row.size.size_id,
                "size": row.size.size,
            }

            response.append(dog)

        return jsonify(response)

    else:
        response = {"message": "Dogs Not Found"}
        return response, 404


# Create / Edit Dog


@dog_bp.route("/dog", methods=["POST"])
@token_required
def post_dog(current_user):
    """Create or edit dog info"""
    content = request.json
    user_id = current_user.user_id

    # If dog_id not in body then they are trying to create
    # If dog_id in body then updating content
    if "dog_id" in content.keys(): 
        queried_dog = (
            db.session.query(Dog).filter(Dog.dog_id == content["dog_id"]).filter(Dog.owner_id == user_id).first()
        )
        if queried_dog:
            breakpoint()
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

            response = process_record(queried_dog)
            response["breed"] = queried_dog.breed.breed_name
            response["size"] = queried_dog.size.size
            response["temperament_type"] = queried_dog.temperament.temperament_type

            return response

        else:
            response = {"message": "Dog Not Found"}
            return response, 404

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

        queried_dog = (
            db.session.query(Dog)
            .join(Breed)
            .join(User)
            .filter(Dog.dog_id == new_dog.dog_id)
            .first()
        )
        response = process_record(queried_dog)
        response["breed"] = queried_dog.breed.breed_name
        response["size"] = queried_dog.size.size
        response["temperament_type"] = queried_dog.temperament.temperament_type

        return response, 201


# Delete Dog


@dog_bp.route("/dog/<dog_id>", methods=["DELETE"])
def delete_dog(dog_id):
    queried_dog = db.session.query(Dog).filter(Dog.dog_id == dog_id).first()

    if queried_dog:
        db.session.delete(queried_dog)
        db.session.commit()

        return {"message": f"Success!"}, 410

    else:
        response = {"message": "Dog Not Found"}
        return response, 404
