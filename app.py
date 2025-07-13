from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os

app = Flask(__name__)

TOGETHER_API_KEY = "01dba539b9f171112f731c99cbc31754b69dd57fcf335786b99544c223be7f91"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"

app.secret_key = TOGETHER_API_KEY

CHAT_HISTORY_FILE = "chat_history.json"
if not os.path.exists(CHAT_HISTORY_FILE):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump([], f)

def save_chat(user_message, bot_reply):
    with open(CHAT_HISTORY_FILE, "r") as f:
        all_chats = json.load(f)
    chat_idx = session.get("chat_idx", 0)
    while len(all_chats) <= chat_idx:
        all_chats.append([])
    all_chats[chat_idx].append({"user": user_message, "bot": bot_reply})
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(all_chats, f, indent=4)

def get_recent_chat_history(user_message, max_turns=5):
    return [user_message]

@app.route("/")
def index():
    if "chat_idx" not in session:
        session["chat_idx"] = 0
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json["message"]
    try:
        history_texts = get_recent_chat_history(user_message)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Always answer ONLY the user's latest question as clearly and directly as possible. "
                    "Ignore unrelated previous context. "
                    "If the user's question is ambiguous, ask for clarification. "
                    "Do not hallucinate or invent information. "
                    "Format your answers in a structured way (such as bullet points, numbered steps, or tables) instead of a paragraph, whenever possible."
                )
            }
        ]
        for text in history_texts:
            messages.append({"role": "user", "content": text})

        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1500,
            "top_p": 1,
            "stop": None
        }

        response = requests.post(
            TOGETHER_API_URL,
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            bot_reply = data["choices"][0]["message"]["content"].strip()
            while "<think>" in bot_reply and "</think>" in bot_reply:
                start = bot_reply.find("<think>")
                end = bot_reply.find("</think>") + len("</think>")
                bot_reply = (bot_reply[:start] + bot_reply[end:]).strip()
        else:
            print("Together API error:", response.status_code, response.text)
            if response.status_code == 500:
                bot_reply = "Sorry, I'm having trouble answering right now. Please try again later."
            else:
                bot_reply = f"Error: {response.status_code} {response.text}"

    except Exception as e:
        print("Exception in /ask:", e)
        bot_reply = f"Error: {e}"

    save_chat(user_message, bot_reply)
    return jsonify({"bot": bot_reply})

@app.route("/delete_history", methods=["POST"])
def delete_history():
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump([], f)
    session["chat_idx"] = 0
    return jsonify({"status": "History cleared"})

@app.route("/past_chats", methods=["GET"])
def past_chats():
    with open(CHAT_HISTORY_FILE, "r") as f:
        all_chats = json.load(f)
    return jsonify({"chats": all_chats})

@app.route("/select_chat", methods=["POST"])
def select_chat():
    idx = request.json.get("chat_idx", 0)
    with open(CHAT_HISTORY_FILE, "r") as f:
        all_chats = json.load(f)
    if 0 <= idx < len(all_chats):
        session["chat_idx"] = idx
        return jsonify({"status": "ok", "chat": all_chats[idx]})
    else:
        return jsonify({"status": "error", "message": "Invalid chat index"}), 400

@app.route("/delete_chat", methods=["POST"])
def delete_chat():
    idx = request.json.get("chat_idx", 0)
    with open(CHAT_HISTORY_FILE, "r") as f:
        all_chats = json.load(f)
    if 0 <= idx < len(all_chats):
        del all_chats[idx]
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump(all_chats, f, indent=4)
        if session.get("chat_idx", 0) == idx:
            session["chat_idx"] = 0
        return jsonify({"status": "deleted"})
    else:
        return jsonify({"status": "error", "message": "Invalid chat index"}), 400

@app.route("/new_chat", methods=["POST"])
def new_chat():
    with open(CHAT_HISTORY_FILE, "r") as f:
        all_chats = json.load(f)
    all_chats.append([])
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(all_chats, f, indent=4)
    session["chat_idx"] = len(all_chats) - 1
    return jsonify({"status": "new chat started", "chat_idx": session["chat_idx"], "chat": []})

if __name__ == "__main__":
    app.run(debug=True)