from flask import Blueprint, jsonify
from flask_cors import cross_origin
from sniffr.models import Size, db, process_records
from flask_cors import cross_origin

size_bp = Blueprint("size_bp", __name__)


@size_bp.route("/sizes", methods=["GET"])
@cross_origin()
def get_size():
    """Get all sizes"""
    all_sizes = db.session.query(Size).all()

    response = []
    if all_sizes:
        for size in all_sizes:
            size_record = {"size_id": size.size_id, "size": size.size}

            response.append(size_record)

        return jsonify(response)

    else:
        response = {"message": "Sizes Not Found"}
        return response, 404
