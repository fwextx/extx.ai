import os
import json
import uuid
from flask import Flask, request, jsonify, render_template
from gpt4all import GPT4All
from flask import abort

app = Flask(__name__)
HISTORY_DIR = "chat_history"
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")

os.makedirs(HISTORY_DIR, exist_ok=True)

# ✅ Initialize GPT4All model globally (only once)
# Make sure the model file name matches your download
model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

def generate_title_from_prompt(message):
    title_prompt = f"Summarize this message as a short 3-5 word chat title:\n\nUser: {message}\n\nTitle:"
    title = generate_with_stop(model, title_prompt, max_tokens=15, stop_tokens=["\n"])
    return title.strip().strip('"')  # clean up quotes or line breaks

@app.route("/api/chats")
def get_chats():
    device_id = request.args.get("device_id")
    if not device_id:
        return jsonify({"error": "device_id required"}), 400

    history = load_history()
    device_chats = history.get(device_id, {})

    chat_list = []
    for chat_id, chat_data in device_chats.items():
        title = chat_data.get("title") or "(No title)"
        chat_list.append({"chat_id": chat_id, "title": title})

    return jsonify({"chats": chat_list})

@app.route("/api/chat", methods=["DELETE"])
def delete_chat():
    data = request.get_json(force=True)
    device_id = data.get("device_id")
    chat_id = data.get("chat_id")

    if not device_id or not chat_id:
        return jsonify({"error": "device_id and chat_id required"}), 400

    history = load_history()
    device_chats = history.get(device_id, {})

    if chat_id not in device_chats:
        return jsonify({"error": "Chat not found"}), 404

    del device_chats[chat_id]
    save_history(history)

    return jsonify({"message": "Chat deleted"})

@app.route("/api/chat")
def get_chat_messages():
    device_id = request.args.get("device_id")
    chat_id = request.args.get("chat_id")
    if not device_id or not chat_id:
        return jsonify({"error": "device_id and chat_id required"}), 400

    history = load_history()
    device_chats = history.get(device_id, {})
    chat = device_chats.get(chat_id, {})
    messages = chat.get("messages", [])

    return jsonify({"messages": messages})

def generate_with_stop(model, prompt, max_tokens=200, stop_tokens=None):
    response = model.generate(prompt, max_tokens=max_tokens)
    if stop_tokens:
        # Find earliest stop token occurrence and truncate
        for stop_token in stop_tokens:
            idx = response.find(stop_token)
            if idx != -1:
                response = response[:idx]
    return response.strip()


@app.route("/api/chat", methods=["POST"])
def post_chat_message():
    data = request.get_json(force=True)
    device_id = data.get("device_id")
    message = data.get("message")
    chat_id = data.get("chat_id")

    if not device_id or not message:
        return jsonify({"error": "device_id and message required"}), 400

    history = load_history()
    device_chats = history.setdefault(device_id, {})

    # Create new chat if chat_id missing or invalid
    if not chat_id or chat_id not in device_chats:
        title = generate_title_from_prompt(message)
        chat_id = uuid.uuid4().hex[:8]
        device_chats[chat_id] = {
            "title": title or message[:20],  # fallback to message snippet
            "messages": []
        }

    chat = device_chats[chat_id]

    # Append user message to this chat only
    chat["messages"].append({"role": "user", "text": message})
    print(f"[{device_id}] [{chat_id}] has said: {message}")
    # Build prompt from this chat’s last messages only
    recent_msgs = chat["messages"][-4:]
    prompt = "You are a helpful assistant.\n"
    for m in recent_msgs:
        role = "User" if m["role"] == "user" else "Assistant"
        prompt += f"{role}: {m['text']}\n"
    prompt += "Assistant:"

    # Generate response for this prompt only
    bot_response = generate_with_stop(model, prompt, max_tokens=1000, stop_tokens=["User:", "Assistant:"])

    # Append bot response to this chat only
    chat["messages"].append({"role": "bot", "text": bot_response})

    save_history(history)

    return jsonify({"chat_id": chat_id, "response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
