from flask import Blueprint, jsonify
from sniffr.models  import Breed, db, process_records

breed_bp = Blueprint("breed_bp", __name__)

@breed_bp.route('/breeds', methods=['GET'])
def get_breed():
    """Get all breeds"""
    all_breeds = db.session.query(Breed).all()

    response = []
    if all_breeds:
        for breed in all_breeds:
            breed_record = {
                'breed_id': breed.breed_id,
                'breed_name': breed.breed_name
                }
            
            response.append(breed_record)

        return jsonify(response)

    else:
        response = {"message": "Breeds Not Found"}
        return response, 404