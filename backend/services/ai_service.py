"""
AI Hospital Receptionist System - AI Service (Ollama Powered)
Fully offline, production-ready AI using local LLM
"""

import requests
import logging

logger = logging.getLogger("AI_SERVICE")

# ----------------------------
# Ollama Config
# ----------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # change if needed

# ----------------------------
# System Prompt
# ----------------------------
SYSTEM_PROMPT = """
You are an AI Hospital Receptionist.

Responsibilities:
- Greet patients politely
- Help with appointment booking
- Answer hospital-related queries
- Handle emergencies properly

Rules:
- NEVER give medical diagnosis
- NEVER prescribe medicines
- In emergencies, tell user to contact hospital immediately
- Keep responses short, clear, professional
"""

# ----------------------------
# Intent Detection
# ----------------------------
def detect_intent(message: str):
    msg = message.lower()

    if any(word in msg for word in ["emergency", "urgent", "help", "dying"]):
        return "emergency"

    if any(word in msg for word in ["appointment", "book", "schedule"]):
        return "appointment"

    if any(word in msg for word in ["hello", "hi", "hey"]):
        return "greeting"

    return "general"


# ----------------------------
# Fallback (still useful)
# ----------------------------
def fallback_response(intent, patient):
    name = patient["first_name"] if patient else "there"

    if intent == "greeting":
        return f"Hello {name}, how can I assist you today?"

    if intent == "appointment":
        return f"Sure {name}, please tell me your preferred date and department."

    if intent == "emergency":
        return "⚠️ This is an emergency. Please contact the hospital immediately."

    return "Could you please provide more details?"


# ----------------------------
# Build Prompt for Ollama
# ----------------------------
def build_prompt(message, history, patient):
    prompt = SYSTEM_PROMPT + "\n\n"

    if patient:
        prompt += f"""
Patient Info:
Name: {patient.get("full_name")}
Age: {patient.get("age")}
Gender: {patient.get("gender")}
"""

    prompt += "\nConversation:\n"

    for msg in history[-5:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        prompt += f"{role}: {msg['message']}\n"

    prompt += f"User: {message}\nAssistant:"

    return prompt


# ----------------------------
# Ollama Call
# ----------------------------
def generate_ollama_response(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    return response.json()["response"].strip()


# ----------------------------
# Main Function
# ----------------------------
def generate_ai_response(message: str, history=None, patient=None):
    if history is None:
        history = []

    intent = detect_intent(message)
    logger.info(f"[AI] Intent: {intent}")

    # Emergency override
    if intent == "emergency":
        return fallback_response(intent, patient)

    try:
        prompt = build_prompt(message, history, patient)
        return generate_ollama_response(prompt)
    except Exception as e:
        logger.error(f"Ollama failed: {e}")
        return fallback_response(intent, patient)