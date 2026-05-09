import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class GroqClient:

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

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
            "temperature": 0.3,
            "max_tokens": 500
        }

        try:
            response = requests.post(
                GroqClient.BASE_URL,
                json=payload,
                headers=headers,
                timeout=30
            )

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except Exception as e:
            print("Groq Error:", e)

            return "AI generation failed"