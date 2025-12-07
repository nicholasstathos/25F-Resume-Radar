from flask import Blueprint, jsonify, request

# Single unified blueprint for ALL of Anya's routes
anya_bp = Blueprint("anya_bp", __name__)


@anya_bp.route("/hallucinations", methods=["GET"])
def hallucination_stats():
    data = [
        {"category": "Overclaiming", "count": 42},
        {"category": "Incorrect Company Facts", "count": 28},
        {"category": "Fabricated Skills", "count": 13},
        {"category": "Wrong Experience Level", "count": 19},
    ]
    return jsonify(data), 200



@anya_bp.route("/employers", methods=["GET"])
def employer_analytics():
    data = [
        {"employer": "Google", "avg_score": 88},
        {"employer": "Amazon", "avg_score": 82},
        {"employer": "Meta", "avg_score": 91},
        {"employer": "Microsoft", "avg_score": 85},
    ]
    return jsonify(data), 200



@anya_bp.route("/universities", methods=["GET"])
def university_analytics():
    data = [
        {"university": "Northeastern University", "avg_score": 86},
        {"university": "MIT", "avg_score": 93},
        {"university": "Harvard", "avg_score": 90},
        {"university": "Boston University", "avg_score": 81},
    ]
    return jsonify(data), 200



@anya_bp.route("/abtests", methods=["GET"])
def get_ab_test_results():
    data = [
        {"test": "Resume Tone", "variant": "A", "conversion": 0.42},
        {"test": "Resume Tone", "variant": "B", "conversion": 0.51},
        {"test": "Skill Extraction Accuracy", "variant": "A", "conversion": 0.61},
        {"test": "Skill Extraction Accuracy", "variant": "B", "conversion": 0.57},
    ]
    return jsonify(data), 200

# this is just in-memory for now; it resets when backend restarts
FEEDBACK_DATA = []


@anya_bp.route("/feedback", methods=["GET"])
def get_feedback():
    return jsonify(FEEDBACK_DATA), 200


@anya_bp.route("/feedback", methods=["POST"])
def submit_feedback():
    body = request.get_json(silent=True) or {}
    message = body.get("message", "").strip()
    user = (body.get("user") or "").strip() or "Anonymous"

    if not message:
        return jsonify({"error": "message is required"}), 400

    entry = {"user": user, "message": message}
    FEEDBACK_DATA.append(entry)

    return jsonify({"status": "ok", "feedback": entry}), 201
