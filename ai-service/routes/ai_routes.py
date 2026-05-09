from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from services.prompt_loader import load_prompt
from datetime import datetime

ai_bp = Blueprint("ai_bp", __name__)

@ai_bp.route("/describe", methods=["POST"])
def describe():

    data = request.json
    text = data.get("text")

    prompt = load_prompt("prompts/describe_prompt.txt")

    result = GroqClient.generate(prompt, text)

    return jsonify({
        "success": True,
        "generated_at": datetime.now().isoformat(),
        "response": result
    })