from flask import Blueprint, jsonify
from sniffr.models  import Temperament, db, process_records

temperament_bp = Blueprint("temperament_bp", __name__)

@temperament_bp.route('/temperaments', methods=['GET'])
def get_temperaments():
    """Get temperament list from the table"""
    temperament_list = db.session.query(Temperament).all()
    temperament_list = process_records(temperament_list)

    return jsonify(temperament_list)