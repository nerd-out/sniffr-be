from flask import Blueprint, request, jsonify
from flask import current_app as app
from sniffr.models import db, Activity, process_records, process_record

# Blueprint Configuration
activity_bp = Blueprint("activity_bp", __name__)

# ---- Routes for the Activity Model ----


@activity_bp.route("/activities", methods=["GET"])
def get_activities():
    """Get all activities"""
    queried_activity = db.session.query(Activity).all()
    queried_activity = process_records(queried_activity)
    return jsonify(queried_activity)


@activity_bp.route("/activity/<activity_id>", methods=["GET"])
def get_activity(activity_id):
    """Get a specific activity by id."""
    activity_id = int(activity_id)
    queried_activity = (
        db.session.query(Activity).filter_by(activity_id=activity_id).all()
    )
    queried_activity = process_records(queried_activity)
    return jsonify(queried_activity)


@activity_bp.route("/activity", methods=["POST"])
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
    return jsonify(process_record(queried_activity))


@activity_bp.route("/activity/<activity_id>", methods=["DELETE"])
def delete_activity(activity_id):
    """Delete a specific activity by id."""
    activity_id = int(activity_id)
    queried_activity = (
        db.session.query(Activity).filter_by(activity_id=activity_id).first()
    )
    db.session.delete(queried_activity)
    db.session.commit()
    return jsonify({"message": "Activity deleted"})
