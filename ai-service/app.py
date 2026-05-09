from flask import Flask
from flask_cors import CORS
from routes.ai_routes import ai_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(ai_bp)

@app.route("/")
def home():
    return {
        "message": "AI Service Running"
    }

@app.route("/health")
def health():

    return {
        "status": "UP",
        "service": "Policy Compliance Testing AI",
        "model": "llama-3.3-70b-versatile"
    }

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )