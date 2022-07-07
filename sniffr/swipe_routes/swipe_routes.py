from concurrent.futures import process
from flask import Blueprint, request, jsonify, current_app as app
from flask_cors import cross_origin
from sniffr.models import db, Swipe, process_records

# Blueprint Configuration
swipe_bp = Blueprint("swipe_bp", __name__)


@swipe_bp.route("/swipe/<swipe_id>", methods=["GET"])
@cross_origin()
def get_swipe(swipe_id):
    swipe_id = int(swipe_id)

    queried_swipe = db.session.query(Swipe).filter_by(swipe_id=swipe_id).first()
    queried_swipe = process_records(queried_swipe)

    return jsonify(queried_swipe)

