from concurrent.futures import process
from flask import Blueprint, request, jsonify, make_response
from flask import current_app as app
from flask_cors import cross_origin
from sniffr.models import Dog, process_records, db

# Blueprint Configuration
dog_bp = Blueprint("dog_bp", __name__)


@dog_bp.route("/dog/<dog_id>", methods=["GET"])
@cross_origin()
def get_dog(dog_id):
    dog_id = int(dog_id)

    queried_dog = db.session.query(Dog).filter_by(dog_id=dog_id).all()
    if queried_dog:
        queried_dog = process_records(queried_dog)
        return jsonify(queried_dog)
    else:
        payload = jsonify({"Status": 404, 
        "Message": "Dog Not Found", 
        "Success": False})
        return make_response(payload, 400)


@dog_bp.route("/dog", methods=["POST"])
@cross_origin()
def post_dog():
    content = request.json

    # If dog_id not in body then they are trying to create
    # If dog_id in body then updating content
    if content["dog_id"]:
        # update dog
        ...

    else:
        # create dog
        dog_name = content["dog_name"]
        user_id = content["user_id"]
        breed_id = content["breed_id"]
        size_id = content["size_id"]
        temperament_id = content["temperament_id"]
        age = content["age"]
        sex = content["sex"]
        is_vaccinated = content["is_vaccinated"]
        is_fixed = content["is_fixed"]

        new_dog = Dog(
            dog_name=dog_name,
            user_id=user_id,
            breed_id=breed_id,
            size_id=size_id,
            temperament_id=temperament_id,
            age=age,
            sex=sex,
            is_vaccinated=is_vaccinated,
            is_fixed=is_fixed,
        )
        db.session.add(new_dog)
        db.session.commit()

        queried_dog = db.session.query(Dog).filter_by(dog_id=new_dog.dog_id).first()
        queried_dog = process(queried_dog)

        return jsonify(queried_dog)
