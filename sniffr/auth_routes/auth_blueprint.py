from flask import Blueprint, request
from flask_cors import cross_origin
from sniffr.models import User, db

# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    """ When a correct email and password is given, provide a success prompt"""
    content = request.json
    email = content['email']
    passwd = content['password']

    # Make sure 
    if email and passwd:
        exists = db.session.query(User.user_id).filter_by(email=f'{email}', password=f'{passwd}').first() is not None

        if exists:
            return {'message': 'success!'}
        
        else:
            return {'message': 'fail'}, 400

    else:
        return {'message': 'fail'}, 400


@auth_bp.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    ''' Simulates a logout point. Doesn't do much until json webtokens are added'''

    return {'message': 'success!'}