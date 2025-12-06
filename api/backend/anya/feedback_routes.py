from flask import Blueprint, request, jsonify

anya_feedback_bp = Blueprint("anya_feedback_bp", __name__)

feedback_list = [
    {"user": "Sarah", "message": "Great resume scoring!", "rating": 5},
    {"user": "Jason", "message": "Dashboard looks clean.", "rating": 4},
]

@anya_feedback_bp.route("/feedback", methods=["GET"])
def get_feedback():
    return jsonify(feedback_list), 200

@anya_feedback_bp.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()

    if not data or "user" not in data or "message" not in data or "rating" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    feedback_list.append({
        "user": data["user"],
        "message": data["message"],
        "rating": data["rating"]
    })

    return jsonify({"status": "Feedback submitted"}), 201
