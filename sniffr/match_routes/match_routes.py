from lib2to3.pgen2 import token
from flask import Blueprint, jsonify, request
from sniffr.models import db, process_records, token_required, process_record, Match, Dog, Swipe


# Blueprint Configuration
match_bp = Blueprint("match_bp", __name__)

# Get all user's matches
@match_bp.route("/matches", methods=["GET"])
@token_required
def get_matches(current_user):
    # Accept user token
    # THEN return up to 3 potential dogs that can be swiped
    # Query and get dogs given a user id

    user_id = current_user.user_id

    past_matches = (
        db.session.query(Match)
        .filter((Match.dog_id_one == )|(Match.dog_id_two == False))
        .filter(Dog.owner_id == user_id)
        .all()
    )

    past_swipes = process_records(past_matches)

    return jsonify(past_swipes)