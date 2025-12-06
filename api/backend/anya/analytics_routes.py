from flask import Blueprint, jsonify


anya_analytics_bp = Blueprint("anya_analytics_bp", __name__)


@anya_analytics_bp.route("/hallucinations", methods=["GET"])
def hallucination_stats():
    data = [
        {"category": "Overclaiming", "count": 42},
        {"category": "Incorrect Company Facts", "count": 28},
        {"category": "Fabricated Skills", "count": 13},
        {"category": "Wrong Experience Level", "count": 19},
    ]
    return jsonify(data), 200


@anya_analytics_bp.route("/employers", methods=["GET"])
def employer_analytics():
    data = [
        {"employer": "Google", "avg_score": 88},
        {"employer": "Amazon", "avg_score": 82},
        {"employer": "Meta", "avg_score": 91},
        {"employer": "Microsoft", "avg_score": 85},
    ]
    return jsonify(data), 200


@anya_analytics_bp.route("/universities", methods=["GET"])
def university_analytics():
    data = [
        {"university": "Northeastern University", "avg_score": 86},
        {"university": "MIT", "avg_score": 93},
        {"university": "Harvard", "avg_score": 90},
        {"university": "Boston University", "avg_score": 81},
    ]
    return jsonify(data), 200
