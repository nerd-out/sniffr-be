from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_cors import cross_origin
from sniffr.models import db, User

# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    content = request.json
    email = content['email']
    passwd = content['password']

    # Make sure 
    if email and passwd:
        exists = db.session.query(User.user_id).filter_by(email=f'{email}', password=f'{passwd}').first() is not None
        
        if exists:
            return jsonify({'status': 'success!'})
        
        else:
            return jsonify({'status': 'fail'})

    else:
        return jsonify({'status': 'fail'})