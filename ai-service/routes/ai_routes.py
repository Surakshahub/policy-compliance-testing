from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import time

from services.groq_client import GroqClient
from services.prompt_loader import load_prompt
from services.cache_service import CacheService

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

        cached = CacheService.get(text)

        if cached:

            cached["cached"] = True

            return jsonify(cached), 200

        prompt = load_prompt("prompts/describe_prompt.txt")

        start_time = time.time()

        result = GroqClient.generate(prompt, text)

        response_time = round(time.time() - start_time, 2)

        response_data = {
            "success": True,
            "generated_at": datetime.now().isoformat(),
            "is_fallback": result["is_fallback"],
            "cached": False,
            "response_time_seconds": response_time,
            "input": text,
            "description": result["content"]
        }

        CacheService.set(text, response_data)

        return jsonify(response_data), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@ai_bp.route("/recommend", methods=["POST"])
def recommend():

    try:

        data = request.get_json()

        text = data.get("text")

        cached = CacheService.get(text)

        if cached:

            cached["cached"] = True

            return jsonify(cached), 200

        prompt = load_prompt("prompts/recommend_prompt.txt")

        start_time = time.time()

        result = GroqClient.generate(prompt, text)

        response_time = round(time.time() - start_time, 2)

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

        response_data = {
            "success": True,
            "generated_at": datetime.now().isoformat(),
            "is_fallback": result["is_fallback"],
            "cached": False,
            "response_time_seconds": response_time,
            "input": text,
            "recommendations": recommendations
        }

        CacheService.set(text, response_data)

        return jsonify(response_data), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@ai_bp.route("/generate-report", methods=["POST"])
def generate_report():

    try:

        data = request.get_json()

        text = data.get("text")

        cached = CacheService.get(text)

        if cached:

            cached["cached"] = True

            return jsonify(cached), 200

        prompt = load_prompt("prompts/report_prompt.txt")

        start_time = time.time()

        result = GroqClient.generate(prompt, text)

        response_time = round(time.time() - start_time, 2)

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

        response_data = {
            "success": True,
            "generated_at": datetime.now().isoformat(),
            "is_fallback": result["is_fallback"],
            "cached": False,
            "response_time_seconds": response_time,
            "input": text,
            "report": report
        }

        CacheService.set(text, response_data)

        return jsonify(response_data), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500