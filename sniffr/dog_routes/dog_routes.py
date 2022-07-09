from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from sniffr.models import Dog, process_records, db

# Blueprint Configuration
dog_bp = Blueprint("dog_bp", __name__)


@dog_bp.route("/dog/<dog_id>", methods=["GET"])
@cross_origin()
def get_dog(dog_id):
    """ Get dog info"""
    dog_id = int(dog_id)

    queried_dog = db.session.query(Dog).filter_by(dog_id=dog_id).all()
    if queried_dog:
        response = process_records(queried_dog)
        response = jsonify(response)
        return response

    else:
        response = {"message": "Dog Not Found"}
        return response, 400


@dog_bp.route("/dog", methods=["POST"])
@cross_origin()
def post_dog():
    """ Create or edit dog info """
    content = request.json

    # If dog_id not in body then they are trying to create
    # If dog_id in body then updating content
    if "dog_id" in content.keys():
        queried_dog = db.session.query(Dog).filter_by(dog_id=content['dog_id']).all()
        if queried_dog:
            # update dog
            response = {"message": f"Successfully pinged API but editing dog id #{content['dog_id']} is not available yet."}
            return response
        
        else:
            response = {"message": "Dog Not Found"}
            return response

    else:
        # create dog
        dog_name = content["dog_name"]
        user_id = content["user_id"]
        age = content["age"]
        sex = content["sex"]

        new_dog = Dog(
            dog_name=dog_name,
            user_id=user_id,
            age=age,
            sex=sex,
        )
        db.session.add(new_dog)
        db.session.commit()

        queried_dog = db.session.query(Dog).filter_by(dog_id=new_dog.dog_id).all()
        queried_dog = process_records(queried_dog)
        return queried_dog
