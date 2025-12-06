from flask import Blueprint, jsonify

anya_abtest_bp = Blueprint("anya_abtest_bp", __name__)

@anya_abtest_bp.route("/abtests", methods=["GET"])
def abtest_results():
    data = [
        {"version": "A", "engagement": 0.76, "conversion": 0.24},
        {"version": "B", "engagement": 0.82, "conversion": 0.31},
    ]
    return jsonify(data), 200
