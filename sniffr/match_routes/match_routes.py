from lib2to3.pgen2 import token
from flask import jsonify
from psutil import users
from flask import Blueprint, jsonify, request
from sniffr.models import db, get_users_dogs_id, token_required, Match, Dog, User, process_dogs


# Blueprint Configuration
match_bp = Blueprint("match_bp", __name__)

# Get all user's matches
@match_bp.route("/matches", methods=["GET"])
@token_required
def get_matches(current_user):
    # Accept user token
    # THEN return all dogs that are matches

    user_id = int(current_user.user_id)
    users_dog_id = get_users_dogs_id(user_id)

    try:
        past_matches = (
        db.session.query(Match)
        .filter((Match.dog_id_two == users_dog_id) | (Match.dog_id_one == users_dog_id))
        .all()
    )

    except:
        return jsonify([])

    

    matched_dog_ids1 = list(set([matched_dog.dog_id_one for matched_dog in past_matches]))
    matched_dog_ids2 = list(set([matched_dog.dog_id_two for matched_dog in past_matches]))
    matched_dog_ids = matched_dog_ids1 + matched_dog_ids2

    matched_dogs = (
            db.session.query(Dog)
            .join(User, Dog.owner_id == User.user_id)
            .filter(Dog.dog_id.in_(matched_dog_ids))
            .filter(Dog.dog_id != users_dog_id)
            .all()
            )

    if matched_dogs:
        response = process_dogs(matched_dogs)
        return jsonify(response)
    else:
        return jsonify([])
