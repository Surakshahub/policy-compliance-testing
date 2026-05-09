from flask import Blueprint, request, jsonify
from datetime import datetime

from services.groq_client import GroqClient
from services.prompt_loader import load_prompt

ai_bp = Blueprint("ai_bp", __name__)


@ai_bp.route("/describe", methods=["POST"])
def describe():

    try:

        data = request.get_json()

        # Validate request body
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400

        text = data.get("text")

        # Validate text field
        if not text:
            return jsonify({
                "success": False,
                "error": "text field is required"
            }), 400

        if len(text.strip()) < 5:
            return jsonify({
                "success": False,
                "error": "Input too short"
            }), 400

        # Load prompt
        prompt = load_prompt("prompts/describe_prompt.txt")

        if not prompt:
            return jsonify({
                "success": False,
                "error": "Prompt loading failed"
            }), 500

        # Generate AI response
        result = GroqClient.generate(prompt, text)

        if not result["success"]:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 500

        # Final response
        return jsonify({
            "success": True,
            "generated_at": datetime.now().isoformat(),
            "input": text,
            "description": result["content"]
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500