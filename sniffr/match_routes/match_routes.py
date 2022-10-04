from lib2to3.pgen2 import token
from flask import jsonify
from psutil import users
from flask import Blueprint, jsonify, request
from sniffr.models import db, get_users_dogs_id, token_required, Match, Dog, User, process_dogs, Swipe


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


@match_bp.route("/matches", methods=["DELETE"])
@token_required
def delete_match(current_user):
    """Deletes a match and they constituant swipes"""
    user_id = int(current_user.user_id)
    content = request.json
    matched_dog_id = int(content['matched_dog_id'])

    queried_match = db.session.query(Match).filter(Match.dog_id_two == matched_dog_id).first()

    if queried_match:
        matched_dog_one = queried_match.dog_id_one
        matched_dog_two = queried_match.dog_id_two

        swipe_one = db.session.query(Swipe).filter(Swipe.swiped_dog_id == matched_dog_one).first()
        swipe_two = db.session.query(Swipe).filter(Swipe.swiped_dog_id == matched_dog_two).first()
    
        db.session.delete(queried_match)
        db.session.delete(swipe_one)
        db.session.delete(swipe_two)

        db.session.commit()

        return jsonify({}), 200

    else:
        return jsonify({'error': "Match not deleted"}), 400
