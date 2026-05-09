import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class GroqClient:

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    @staticmethod
    def fallback_response():

        return {
            "success": True,
            "is_fallback": True,
            "content": "Fallback response generated because AI service is temporarily unavailable."
        }

    @staticmethod
    def generate(prompt, user_input):

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "temperature": 0.2,
            "max_tokens": 200
        }

        try:

            response = requests.post(
                GroqClient.BASE_URL,
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code != 200:

                return GroqClient.fallback_response()

            data = response.json()

            ai_response = data["choices"][0]["message"]["content"]

            return {
                "success": True,
                "is_fallback": False,
                "content": ai_response.strip()
            }

        except Exception as e:

            print("Groq Error:", e)

            return GroqClient.fallback_response()