# 🏥 AI Hospital Receptionist System

An advanced, locally-hosted AI hospital receptionist built using Flask and a local LLM (Ollama).
This system simulates a real hospital front desk, capable of interacting with patients, managing queries, and guiding them through symptom descriptions with empathy and professionalism—all while keeping data 100% private on the local machine.

---
**Here is a look at the UI in action:**
![AI Receptionist Chat UI](Final OP2.png)
---

---

## 🚀 Features

- 🤖 Local AI Inference: Powered by Ollama (llama3.2:1b) for lightning-fast, private responses.
- 🧠 Context-Aware Memory: Maintains continuous chat history during a session so users don't repeat themselves.
- 💬 Interactive Web UI: A clean, responsive frontend built with HTML/CSS/JS that communicates seamlessly with the backend.
- 🏥 Empathic Triage: Strictly bound by system prompts to ask meaningful follow-ups without providing medical diagnoses.
- ⚡ REST API Architecture: Clean separation of frontend and backend logic.
- 🔒 Privacy First: No external API calls are required, keeping patient interactions fully local.

---

## 🧱 Project Structure

```text
AI-Hospital-Receptionist-System/
│
├── backend/
│   ├── app.py                 (Main Flask application)
│   ├── routes/
│   │   └── chatbot.py         (AI routing and logic)
│   ├── database/
│   │   └── db.py              (SQLite database initialization)
│   └── requirements.txt
│
├── static/                    (Optional CSS/JS files)
├── templates/
│   └── index.html             (The responsive Chat UI)
│
├── data/
│   └── hospital_data.json
├── docs/
│   └── README.md
└── .env

---

## ⚙️ Installation

1. Clone Project
git clone https://github.com/CertifiedSomebody/AI-Hospital-Receptionist-System.git
cd AI-Hospital-Receptionist-System

2. Create Virtual Environment
python -m venv venv

3. Activate Environment
(Windows)
venv\Scripts\activate

(Mac/Linux)
source venv/bin/activate

4. Install Dependencies
pip install -r backend/requirements.txt

---

## 🧠 AI Setup (Ollama - Required for Local Use)

This project uses Meta's hyper-optimized 1B parameter model to run incredibly fast on standard hardware without needing a dedicated GPU.

1. Install Ollama: https://ollama.com/
2. Download and Run the Fast Model: Open a separate terminal and run:
ollama run llama3.2:1b

(Leave this terminal window open in the background while running the Flask app).

---

## 🔑 Environment Variables

Create a .env file in the root directory:

PORT=5000
DEBUG=True
DATABASE_URL=sqlite:///./hospital.db

---

## ▶️ Run the Application

Start the Flask backend server:
python -m backend.app

Once the server is running, open your browser and navigate to: http://127.0.0.1:5000

---

## 🌐 API Endpoints

Base URL: http://127.0.0.1:5000

- Chat Endpoint: POST /api/chatbot/chat
  (Request Example: {"message": "I am feeling a bit under the weather", "session_id": "12345"})
- Get Chat History: GET /api/chatbot/history/<session_id>
- Reset Chat: POST /api/chatbot/reset/<session_id>
- Health Check: GET /health

---

## 🧪 Sample Use Cases

- Ask hospital timings
- Request assistance describing symptoms
- Check doctor availability
- Emergency guidance
- General hospital queries

⚠️ Important Notes:
- This system does NOT provide medical diagnosis.
- AI responses are for preliminary triage and assistance only.
- Always advise users to consult a real doctor for medical issues.

---

## 🔮 Future Enhancements

- 📅 Full appointment booking system integration
- 👤 Patient management APIs and persistent patient profiles
- 🧠 Persistent chat memory across server restarts (saving to SQLite)
- 🎤 Voice-enabled receptionist (Speech-to-Text / Text-to-Speech)
- 📊 Admin dashboard for hospital staff

---

## 🧑‍💻 Tech Stack

- Frontend: HTML5, CSS3, Vanilla JavaScript
- Backend: Python, Flask, Flask-CORS
- Database: SQLAlchemy (SQLite)
- AI Engine: Ollama (LLaMA 3.2 1B) / Requests Library

---

### License
This project is for educational and demonstration purposes.

### Author
Prabhatkumar Jha - Developed as an advanced AI-based system simulating a real-world hospital receptionist.
