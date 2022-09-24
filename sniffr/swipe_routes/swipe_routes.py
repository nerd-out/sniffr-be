from lib2to3.pgen2 import token
from flask import Blueprint, jsonify, request
from sniffr.models import db, Swipe, process_records, token_required, Dog, User, process_record


# Blueprint Configuration
swipe_bp = Blueprint("swipe_bp", __name__)


@swipe_bp.route("/swipe/<swipe_id>", methods=["GET"])
def get_swipe(swipe_id):
    swipe_id = int(swipe_id)

    queried_swipe = db.session.query(Swipe).filter_by(swipe_id=swipe_id).first()
    queried_swipe = process_records(queried_swipe)

    return jsonify(queried_swipe)


# Get new dogs to swipe for a user
@swipe_bp.route("/swipes", methods=["GET"])
@token_required
def get_swipes(current_user):
    # Accept user token
    # THEN return up to 3 potential dogs that can be swiped
    # Query and get dogs given a user id

    user_id = current_user.user_id

    past_swipes = (
        db.session.query(Swipe)
        .join(Dog, Dog.dog_id == Swipe.dog_id)
        .filter((Swipe.is_interested == True)|(Swipe.is_interested == False))
        .filter(Dog.owner_id == user_id)
        .all()
    )
    swiped_dogs = [dog.swiped_dog_id for dog in past_swipes]

    possible_dogs = (
        db.session.query(Dog)
        .join(User, Dog.owner_id == User.user_id)
        .filter(Dog.owner_id != user_id)
        .filter(Dog.dog_id.not_in(swiped_dogs))
        .limit(3)
        .all()
    )

    response = []
    if possible_dogs:
        for row in possible_dogs:
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
        return {'message': 'no potential found'}



# Add swipe
@swipe_bp.route("/swipe", methods=["POST"])
@token_required
def swipe_dog(current_user):
    # Accept token and get user id
    user_id = current_user.user_id

    # Read post request containing information on which dog and swipe-type
    content = request.json

    # Find user's first dog
    users_dog = (
        db.session.query(Dog)
        .join(User, Dog.owner_id == User.user_id)
        .filter(Dog.owner_id == user_id)
        .first()
    )
    users_dog = users_dog.dog_id
    
    # Log Swipe
    new_swipe = Swipe(
            dog_id=users_dog,
            swiped_dog_id=content["swiped_dog_id"],
            is_interested=content["is_interested"],
        )
    
    try:
        db.session.add(new_swipe)
        db.session.commit()
        return_json = process_record(new_swipe)
        return return_json

    except:
        db.session.rollback()
        return {'message': 'Unable to add swipe'}
    


# Delete Swipe
@swipe_bp.route("/swipe", methods=["DELETE"])
@token_required
def delete_activity(current_user):
    # Accept token and get user id
    user_id = current_user.user_id

    # Read post request containing information on which swipe
    content = request.json
    swipe_id = int(content['swipe_id'])

    queried_swipe = (
        db.session.query(Swipe).filter_by(swipe_id=swipe_id).first()
    )
    if queried_swipe:
        db.session.delete(queried_swipe)
        db.session.commit()
        return jsonify({"message": "Swipe deleted"})
    else:
        return {"message": "Swipe not found"}