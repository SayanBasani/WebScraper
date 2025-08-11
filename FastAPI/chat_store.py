# chat_store.py
import os
import json
import uuid
from datetime import datetime
import google.generativeai as genai

from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("gmini_api_key")

genai.configure(api_key=api_key)


CHAT_DIR = "chats"
os.makedirs(CHAT_DIR, exist_ok=True)

def save_chat_session(chat_session, title="Untitled Chat"):
    chat_data = {
        "chat_id": str(uuid.uuid4()),
        "title": title,
        "created_at": datetime.utcnow().isoformat(),
        "history": [msg.to_dict() for msg in chat_session.history]
    }

    with open(f"{CHAT_DIR}/{chat_data['chat_id']}.json", "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=2)
    return chat_data["chat_id"]

def list_chat_sessions():
    sessions = []
    for file in os.listdir(CHAT_DIR):
        if file.endswith(".json"):
            with open(f"{CHAT_DIR}/{file}", "r", encoding="utf-8") as f:
                data = json.load(f)
                sessions.append({
                    "chat_id": data["chat_id"],
                    "title": data.get("title", "Untitled"),
                    "created_at": data["created_at"]
                })
    return sessions

def load_chat_session(chat_id):
    filepath = f"{CHAT_DIR}/{chat_id}.json"
    if not os.path.exists(filepath):
        raise FileNotFoundError("Chat session not found")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# main.py

def start_new_chat():
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    chat = model.start_chat(history=[])
    return chat

def resume_old_chat(chat_id):
    data = load_chat_session(chat_id)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    chat = model.start_chat(history=data["history"])
    return chat

def run():
    print("Welcome to Gemini Chat\n")
    print("1. Start new chat")
    print("2. View and resume past chat")
    choice = input("Choose: ")

    if choice == "1":
        chat = start_new_chat()
    elif choice == "2":
        sessions = list_chat_sessions()
        if not sessions:
            print("No previous chats found.")
            return

        print("\nPrevious Chats:")
        for i, s in enumerate(sessions):
            print(f"{i+1}. {s['title']} ({s['created_at']})")

        idx = int(input("Select chat number to resume: ")) - 1
        chat_id = sessions[idx]["chat_id"]
        chat = resume_old_chat(chat_id)
    else:
        print("Invalid choice.")
        return

    print("\nStart chatting (type 'exit' to stop and save):\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            title = input("Enter a title for this chat: ").strip() or "Untitled Chat"
            chat_id = save_chat_session(chat, title)
            print(f"Chat saved with ID: {chat_id}")
            break

        
# run()
chat = start_new_chat()
user_input = input("enter ")
response = chat.send_message(user_input)
print("Gemini:", response.text)
