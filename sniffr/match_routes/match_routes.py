from lib2to3.pgen2 import token
from flask import Blueprint, jsonify, request
from sniffr.models import db, process_records, token_required, process_record, Match, Dog, User


# Blueprint Configuration
match_bp = Blueprint("match_bp", __name__)

# Get all user's matches
@match_bp.route("/matches", methods=["GET"])
@token_required
def get_matches(current_user):
    # Accept user token
    # THEN return up to 3 potential dogs that can be swiped
    # Query and get dogs given a user id

    user_id = int(current_user.user_id)

    past_matches = (
        db.session.query(Match)
        .join(Dog, Match.dog_id_one == Dog.dog_id)  
        .filter(Dog.owner_id == user_id)
        .all()
    )

    # Return list of dogs that are matches
    matched_dog_ids = [match.dog_id_two for match in past_matches]
    matched_dogs = (
            db.session.query(Dog)
            .join(User, Dog.owner_id == User.user_id)
            .filter(Dog.owner_id != user_id)
            .filter(Dog.dog_id.in_(matched_dog_ids))
            .all()
            )

    return jsonify(process_records(matched_dogs))