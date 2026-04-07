import requests
from flask import Blueprint, request, jsonify

chatbot_bp = Blueprint("chatbot", __name__)

# ----------------------------
# Ollama Config
# ----------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"

# IMPORTANT: must match installed model exactly
MODEL_NAME = "llama3.2:1b"

# ----------------------------
# System Prompt
# ----------------------------
SYSTEM_PROMPT = """
You are an AI hospital receptionist assistant.

Your role:
- Help users describe symptoms and guide them
- Ask relevant follow-up questions when needed
- Respond clearly, naturally, and professionally
- Show empathy and understanding

Rules:
- Be concise but helpful
- Do not repeat "provide more details"
- Suggest seeking medical help if symptoms are serious
- Do NOT diagnose
- Ask 1–2 meaningful follow-up questions if needed
"""

# ----------------------------
# Chat Route
# ----------------------------
@chatbot_bp.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    # Handle CORS preflight
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        user_message = data.get("message", "").strip()
        history = data.get("history", [])

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # ----------------------------
        # Build conversation
        # ----------------------------
        conversation = SYSTEM_PROMPT + "\n\n"

        if isinstance(history, list):
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                conversation += f"{role}: {content}\n"

        conversation += f"user: {user_message}\nassistant:"

        # ----------------------------
        # Call Ollama
        # ----------------------------
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": conversation,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 300
                }
            },
            timeout=60
        )

        response.raise_for_status()
        result = response.json()

        # Ollama sometimes returns 'response' OR different structure
        ai_text = result.get("response")

        if not ai_text:
            ai_text = result.get("message", {}).get("content", "")

        ai_text = ai_text.strip()

        if not ai_text:
            ai_text = "Sorry, I couldn't generate a response."

        # ----------------------------
        # Return consistent format
        # ----------------------------
        return jsonify({
            "response": ai_text
        })

    # ----------------------------
    # Ollama / network errors
    # ----------------------------
    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Ollama not running. Start it with: ollama run llama3"
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "AI request timed out"
        }), 504

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "AI service unavailable",
            "details": str(e)
        }), 503

    # ----------------------------
    # General errors
    # ----------------------------
    except Exception as e:
        print(f"Backend Crash: {e}") # This will print in your VS Code terminal
        return jsonify({
            "error": "Unexpected server error",
            "details": str(e)
        }), 500