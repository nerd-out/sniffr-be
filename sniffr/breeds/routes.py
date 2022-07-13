from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from sniffr.breeds.models import Breed, db
from sniffr.models  import process_records

breed_bp = Blueprint("breed_bp", __name__)

@breed_bp.route('/breeds', methods=['GET'])
@cross_origin()
def get_breed():
    """Get all breeds"""
    all_breeds = db.session.query(Breed).all()
    all_breeds = process_records(all_breeds)

    return jsonify(all_breeds)