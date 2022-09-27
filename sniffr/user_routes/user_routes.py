from flask import Blueprint, request
from sniffr.models import User, db, token_required, process_record

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/user", methods=["DELETE"])
@token_required
def delete_user(current_user):
    user_id = current_user.user_id
    queried_user = db.session.query(User).filter(User.user_id == user_id).first()

    if queried_user:
        db.session.delete(queried_user)
        db.session.commit()

        return {}, 200

    else:
        response = {}
        return response, 204


@user_bp.route("/user/edit", methods=["POST"])
@token_required
def edit_user(current_user):
    """Edits a user."""
    content = request.json

    user_id = current_user.user_id
    queried_user = db.session.query(User).filter(User.user_id == user_id).first()

    if queried_user:
        queried_user.email = content["email"]
        queried_user.birthday = content["birthday"]
        queried_user.gender = content["gender"]
        queried_user.max_distance = content["max_distance"]
        queried_user.name = content["name"]
        queried_user.user_bio = content["user_bio"]
        queried_user.zipcode = content["zipcode"]
        queried_user.user_pic = content["user_pic"]

        db.session.commit()

        response = process_record(queried_user)
        return response

    else:
        response = []
        return response, 404
