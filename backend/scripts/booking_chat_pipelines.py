# scripts/booking_chat_pipeline.py
from .chatbot import generate_reply

def chat(user_input: str, history: list) -> str:
    # Append user message to history
    history.append(f"User: {user_input}")
    
    # Generate bot reply
    bot_reply = generate_reply(history)
    
    # Append bot reply
    history.append(f"Bot: {bot_reply}")
    
    return bot_reply