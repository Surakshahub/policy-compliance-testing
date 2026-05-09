from flask import Blueprint, request, jsonify

ai_bp = Blueprint("ai_bp", __name__)

@ai_bp.route("/describe", methods=["POST"])
def describe():
    data = request.json

    return jsonify({
        "success": True,
        "message": "Describe endpoint working",
        "data": data
    })

@ai_bp.route("/recommend", methods=["POST"])
def recommend():
    return jsonify({
        "success": True,
        "message": "Recommend endpoint working"
    })

@ai_bp.route("/generate-report", methods=["POST"])
def generate_report():
    return jsonify({
        "success": True,
        "message": "Generate report endpoint working"
    })