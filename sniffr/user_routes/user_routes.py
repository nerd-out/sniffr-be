from flask import Blueprint
from flask_cors import cross_origin
from sniffr.models import User, db

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/user/<user_id>", methods=["DELETE"])
@cross_origin()
def delete_user(user_id):
    queried_user = db.session.query(User).filter(User.user_id == user_id).first()

    if queried_user:
        db.session.delete(queried_user)
        db.session.commit()

        return {"message": f"Successfully deleted user"}, 410

    else:
        response = {"message": "User Not Found"}
        return response, 404
