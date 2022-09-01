from flask import Blueprint, request, jsonify
from flask import current_app as app
from sniffr.models import db, Activity, process_records
from flask_cors import cross_origin

# Blueprint Configuration
activity_bp = Blueprint("activity_bp", __name__)

# ---- Routes for the Activity Model ----


@activity_bp.route("/activities", methods=["GET"])
@cross_origin()
def get_activities():
    """Get all activities"""
    queried_activity = db.session.query(Activity).all()
    queried_activity = process_records(queried_activity)
    return jsonify(queried_activity)


@activity_bp.route("/activity/<activity_id>", methods=["GET"])
@cross_origin()
def get_activity(activity_id):
    """Get a specific activity by id."""
    activity_id = int(activity_id)
    queried_activity = (
        db.session.query(Activity).filter_by(activity_id=activity_id).all()
    )
    queried_activity = process_records(queried_activity)
    return jsonify(queried_activity)


@activity_bp.route("/activity", methods=["POST"])
@cross_origin()
def post_activity():
    """Create a new activity"""
    content = request.json
    print(content)

    new_activity = Activity(
        activity_description=content["activity_description"],
    )
    db.session.add(new_activity)
    db.session.commit()

    queried_activity = (
        db.session.query(Activity)
        .filter_by(activity_id=new_activity.activity_id)
        .first()
    )
    return jsonify(queried_activity)


@activity_bp.route("/activity/<activity_id>", methods=["DELETE"])
@cross_origin()
def delete_activity(activity_id):
    """Delete a specific activity by id."""
    activity_id = int(activity_id)
    queried_activity = (
        db.session.query(Activity).filter_by(activity_id=activity_id).first()
    )
    db.session.delete(queried_activity)
    db.session.commit()
    return jsonify({"message": "Activity deleted"})
