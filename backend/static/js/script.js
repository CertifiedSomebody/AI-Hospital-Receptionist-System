// AI Hospital Receptionist - Frontend Logic
console.log("🚀 script.js loaded successfully!");

// -----------------------------
// Config
// -----------------------------
// Hardcoded to match your exact browser URL to prevent CORS/Connection issues
const API_BASE = "http://127.0.0.1:5000/api/chatbot"; 
let sessionId = localStorage.getItem("session_id") || null;

// -----------------------------
// DOM Elements
// -----------------------------
const chatContainer = document.getElementById("chat-container");
const inputField = document.getElementById("user-input");

// If you have a Send button, let's try to find it (assuming it has id="send-btn" or similar)
// If your HTML uses a different ID for the button, change "send-btn" below to match it.
const sendButton = document.getElementById("send-btn") || document.querySelector("button");

// -----------------------------
// Utility: Add Message to UI
// -----------------------------
function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.innerText = text;
    chatContainer.appendChild(msg);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// -----------------------------
// Load Previous Chat History
// -----------------------------
async function loadHistory() {
    if (!sessionId) return;
    try {
        console.log(`Loading history for session: ${sessionId}`);
        const res = await fetch(`${API_BASE}/history/${sessionId}`);
        if (!res.ok) return;
        
        const data = await res.json();
        chatContainer.innerHTML = "";
        
        data.history.forEach(msg => {
            addMessage(msg.message, msg.role === "user" ? "user" : "bot");
        });
    } catch (err) {
        console.warn("History load failed:", err);
    }
}

// -----------------------------
// Send Message
// -----------------------------
async function sendMessage() {
    const message = inputField.value.trim();
    if (!message) return;

    addMessage(message, "user");
    inputField.value = "";

    try {
        console.log(`Sending message to: ${API_BASE}/chat`);
        
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });

        const data = await res.json();
        console.log("Server response:", data);

        // Show the actual error Flask sends back
        if (!res.ok) {
            addMessage(`⚠️ Server error: ${data.error || "Unknown issue"}`, "bot");
            return;
        }

        // Save session
        sessionId = data.session_id;
        localStorage.setItem("session_id", sessionId);
        addMessage(data.response, "bot");

    } catch (err) {
        console.error("Fetch request failed entirely!", err);
        addMessage(`⚠️ Network Error: Could not reach the Flask server at ${API_BASE}. Make sure the Python server is running!`, "bot");
    }
}

// -----------------------------
// Reset Chat
// -----------------------------
async function resetChat() {
    if (!sessionId) return;
    try {
        await fetch(`${API_BASE}/reset/${sessionId}`, {
            method: "POST"
        });
        localStorage.removeItem("session_id");
        sessionId = null;
        chatContainer.innerHTML = "";
        addMessage("Chat reset successfully.", "bot");
    } catch (err) {
        console.error("Reset failed:", err);
        addMessage("⚠️ Failed to reset chat.", "bot");
    }
}

// -----------------------------
// Event Listeners & Init App
// -----------------------------

// Listen for the Enter key
inputField.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        e.preventDefault(); // CRITICAL: Stops the page from accidentally refreshing if input is inside a <form>
        sendMessage();
    }
});

// Listen for the Send button click (if it exists)
if (sendButton) {
    sendButton.addEventListener("click", function(e) {
        e.preventDefault(); // CRITICAL: Stops page refresh
        sendMessage();
    });
}

window.onload = () => {
    loadHistory();
    if (!sessionId) {
        addMessage("Hello! I am your AI Hospital Receptionist. How can I help you today?", "bot");
    }
};