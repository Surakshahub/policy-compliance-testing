from flask import Blueprint, request, jsonify
from datetime import datetime
import json

from services.groq_client import GroqClient
from services.prompt_loader import load_prompt
from flask import Blueprint, request, jsonify
from datetime import datetime
import json

ai_bp = Blueprint("ai_bp", __name__)


@ai_bp.route("/describe", methods=["POST"])
def describe():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400

        text = data.get("text")

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

        prompt = load_prompt("prompts/describe_prompt.txt")

        if not prompt:
            return jsonify({
                "success": False,
                "error": "Prompt loading failed"
            }), 500

        result = GroqClient.generate(prompt, text)

        return jsonify({
            "success": True,
            "generated_at": datetime.now().isoformat(),
            "is_fallback": result["is_fallback"],
            "input": text,
            "description": result["content"]
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@ai_bp.route("/recommend", methods=["POST"])
def recommend():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400

        text = data.get("text")

        if not text:
            return jsonify({
                "success": False,
                "error": "text field is required"
            }), 400

        prompt = load_prompt("prompts/recommend_prompt.txt")

        if not prompt:
            return jsonify({
                "success": False,
                "error": "Prompt loading failed"
            }), 500

        result = GroqClient.generate(prompt, text)

        try:
            recommendations = json.loads(result["content"])

        except:
            recommendations = [
                {
                    "action_type": "Fallback",
                    "description": result["content"],
                    "priority": "LOW"
                }
            ]

        return jsonify({
            "success": True,
            "generated_at": datetime.now().isoformat(),
            "is_fallback": result["is_fallback"],
            "input": text,
            "recommendations": recommendations
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    

@ai_bp.route("/generate-report", methods=["POST"])
def generate_report():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400

        text = data.get("text")

        if not text:
            return jsonify({
                "success": False,
                "error": "text field is required"
            }), 400

        prompt = load_prompt("prompts/report_prompt.txt")

        if not prompt:
            return jsonify({
                "success": False,
                "error": "Prompt loading failed"
            }), 500

        result = GroqClient.generate(prompt, text)

        try:
            report = json.loads(result["content"])

        except:
            report = {
                "title": "Fallback Report",
                "summary": result["content"],
                "overview": "AI fallback response generated.",
                "key_items": [],
                "recommendations": []
            }

        return jsonify({
            "success": True,
            "generated_at": datetime.now().isoformat(),
            "is_fallback": result["is_fallback"],
            "input": text,
            "report": report
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500