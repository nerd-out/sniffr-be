from lib2to3.pgen2 import token
from flask import Blueprint, jsonify, request
from sniffr.models import db, process_records, token_required, process_record


# Blueprint Configuration
match_bp = Blueprint("match_bp", __name__)
