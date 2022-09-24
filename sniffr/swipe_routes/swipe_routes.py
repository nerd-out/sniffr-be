from flask import Blueprint, jsonify
from sniffr.models import db, Swipe, process_records, token_required


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
    queried_dogs = (
        db.session.query(Dog)
        .join(User, Dog.owner_id == User.user_id)
        .filter(Dog.owner_id == user_id)
        .all()
    )

    breakpoint()
    


# # Add swipe
# def swipe_dog(current_user):
#     # Accept token and get user id
#     # Return
