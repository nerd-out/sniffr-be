from flask import Blueprint, request
from flask_cors import cross_origin
from sniffr.models import User, db, process_records

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
        # exists = db.session.query(User.user_id).filter_by(email=f'{email}').first()
        result = db.session.query(User).filter_by(email=f'{email}').first()

        if result and result.verify_password(password=passwd):
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

@auth_bp.route('/createuser', methods=['POST'])
@cross_origin()
def create_user():
    ''' Creates a user when a username, password, and email.'''

    content = request.json
    email = content['email']
    passwd = content['password']
    username = content['password']

    new_user = User(
        username=username,
        password=passwd,
        email=email
    )
    db.session.add(new_user)
    db.session.commit()

    # queried_user = db.session.query(User).filter_by(user_id=new_user.user_id).all()
    # queried_user = process_records(queried_user)
    return email