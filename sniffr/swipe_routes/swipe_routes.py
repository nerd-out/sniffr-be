from lib2to3.pgen2 import token
from flask import Blueprint, jsonify, request
from sniffr.models import (
    db,
    Swipe,
    process_records,
    Breed,
    token_required,
    process_dog,
    Dog,
    User,
    process_record,
    Match,
)


# Blueprint Configuration
swipe_bp = Blueprint("swipe_bp", __name__)

# Get one swipe
@swipe_bp.route("/swipe/<swipe_id>", methods=["GET"])
def get_swipe(swipe_id):
    swipe_id = int(swipe_id)

    queried_swipe = db.session.query(Swipe).filter_by(swipe_id=swipe_id).first()
    queried_swipe = process_records(queried_swipe)

    return jsonify(queried_swipe)


# Get all user's swipes
@swipe_bp.route("/pastswipes", methods=["GET"])
@token_required
def get_past_swipes(current_user):
    # Accept user token
    # THEN return up to 3 potential dogs that can be swiped
    # Query and get dogs given a user id

    user_id = current_user.user_id

    past_swipes = (
        db.session.query(Swipe)
        .join(Dog, Dog.dog_id == Swipe.dog_id)
        .filter((Swipe.is_interested == True) | (Swipe.is_interested == False))
        .filter(Dog.owner_id == user_id)
        .all()
    )

    past_swipes = process_records(past_swipes)

    return jsonify(past_swipes)


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
        .filter((Swipe.is_interested == True) | (Swipe.is_interested == False))
        .filter(Dog.owner_id == user_id)
        .all()
    )
    swiped_dogs = [dog.swiped_dog_id for dog in past_swipes]

    possible_dog = (
        db.session.query(Dog)
        .join(User, Dog.owner_id == User.user_id)
        .join(Breed, Dog.breed_id == Breed.breed_id)
        .filter(Dog.owner_id != user_id)
        .filter(Dog.dog_id.not_in(swiped_dogs))
        .first()
    )

    response = {}
    if possible_dog:
        response = process_dog(possible_dog)
        return jsonify(response)
    else:
        return jsonify(response)


# Add swipe
@swipe_bp.route("/swipe", methods=["POST"])
@token_required
def swipe_dog(current_user):
    # Accept token and get user id
    user_id = int(current_user.user_id)

    # Read post request containing information on which dog and swipe-type
    content = request.json

    # Find user's first dog
    users_dog = (
        db.session.query(Dog)
        .join(User, Dog.owner_id == User.user_id)
        .filter(Dog.owner_id == user_id)
        .first()
    )
    if not users_dog:
        return jsonify({"error": "User has no dogs"}), 400

    users_dog = users_dog.dog_id

    # Log Swipe
    new_swipe = Swipe(
        dog_id=users_dog,
        swiped_dog_id=int(content["swiped_dog_id"]),
        is_interested=content["is_interested"],
    )

    try:
        db.session.add(new_swipe)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"error": "Unable to add swipe"}), 400

    # If successful, search for corresponding swipe
    matching_like = (
        db.session.query(Swipe)
        .join(Dog, Swipe.swiped_dog_id == Dog.dog_id)
        .filter(Dog.dog_id == users_dog)
        .filter(Swipe.dog_id == int(content["swiped_dog_id"]))
        .first()
    )

    # If is_interested matching swipe found
    if matching_like:
        if matching_like.is_interested == True:
            # then create match if not one already
            # check for previous match
            new_match = Match(
                dog_id_one=new_swipe.dog_id, dog_id_two=matching_like.dog_id
            )

            try:
                db.session.add(new_match)
                db.session.commit()

            except:
                db.session.rollback()
                return jsonify({"error": "Unable to add match"}), 400

            # Get matched dog info
            matched_dog = (
                db.session.query(Dog)
                .join(User, Dog.owner_id == User.user_id)
                .join(Match, Dog.dog_id == Match.dog_id_two)
                .filter(Dog.dog_id == matching_like.dog_id)
                .first()
            )

            # Return response
            response = {}
            if matched_dog:
                response = process_dog(matched_dog)
                response["match"] = True
                return jsonify(response)

            else:
                return jsonify(response), 200
    else:

        # Return next swipe to front end
        past_swipes = (
            db.session.query(Swipe)
            .join(Dog, Dog.dog_id == Swipe.dog_id)
            .filter((Swipe.is_interested == True) | (Swipe.is_interested == False))
            .filter(Dog.owner_id == user_id)
            .all()
        )
        swiped_dogs = [dog.swiped_dog_id for dog in past_swipes]

        possible_dog = (
            db.session.query(Dog)
            .join(User, Dog.owner_id == User.user_id)
            .filter(Dog.owner_id != user_id)
            .filter(Dog.dog_id.not_in(swiped_dogs))
            .first()
        )

        if possible_dog:
            response = process_dog(possible_dog)
            response["match"] = False
            return jsonify(response)

        else:
            return jsonify({})


# Delete Swipe
@swipe_bp.route("/swipe", methods=["DELETE"])
@token_required
def delete_swipe(current_user):
    # Accept token and get user id
    user_id = int(current_user.user_id)

    # Read post request containing information on which swipe
    content = request.json
    swipe_id = int(content["swipe_id"])

    queried_swipe = db.session.query(Swipe).filter_by(swipe_id=swipe_id).first()

    if queried_swipe:
        db.session.delete(queried_swipe)
        db.session.commit()

        # find match if there is one
        dog1_id = queried_swipe.dog_id
        dog2_id = queried_swipe.swiped_dog_id
        queried_match = (
            db.session.query(Match)
            .filter_by(dog_id_one=dog1_id, dog_id_two=dog2_id)
            .first()
        )
        if queried_match:
            db.session.delete(queried_match)
            db.session.commit()

        return jsonify({}), 200
    else:
        return jsonify({}), 204
