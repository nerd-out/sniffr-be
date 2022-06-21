from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_cors import cross_origin

# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    content = request.json
    payl = [{'message': 'succcess'}]

    return jsonify(payl)
