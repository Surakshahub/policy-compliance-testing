from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import time

from services.groq_client import GroqClient
from services.prompt_loader import load_prompt
from services.cache_service import CacheService
from services.metrics_service import MetricsService
from services.logger_service import LoggerService

ai_bp = Blueprint("ai_bp", __name__)


@ai_bp.route("/describe", methods=["POST"])
def describe():
    """
    Generate compliance description
    ---
    tags:
      - AI Endpoints

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              example: Sensitive customer data exposed publicly

    responses:
      200:
        description: Description generated successfully
    """


@ai_bp.route("/recommend", methods=["POST"])
def recommend():
    """
    Generate compliance recommendations
    ---
    tags:
      - AI Endpoints

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              example: Employee passwords stored in plain text

    responses:
      200:
        description: Recommendations generated successfully
    """
@ai_bp.route("/generate-report", methods=["POST"])
def generate_report():
    """
    Generate compliance report
    ---
    tags:
      - AI Endpoints

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              example: Financial customer data exposed publicly

    responses:
      200:
        description: Report generated successfully
    """
def validate_input(text):

    blocked_patterns = [
        "<script>",
        "</script>",
        "DROP TABLE",
        "SELECT *",
        "--",
        ";"
    ]

    for pattern in blocked_patterns:

        if pattern.lower() in text.lower():

            return False

    return True