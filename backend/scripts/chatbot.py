# scripts/chatbot.py

from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import re                     # <-- NEW import

# Load model once at import time (efficient)
print("Loading AI model...")
tokenizer = T5Tokenizer.from_pretrained(
    "C:/Users/Awoleye/ecom_chatbot/model/my_final_model",
    legacy=False
)
model = T5ForConditionalGeneration.from_pretrained(
    "C:/Users/Awoleye/ecom_chatbot/model/my_final_model"
)
model.eval()
print("Model loaded!")


# --------------------------------------------------------------
# Helper – fixes leading whitespace / invisible chars + capitalises
# --------------------------------------------------------------
def _clean_and_capitalize(reply: str) -> str:
    reply = reply.strip()                                   # drop leading/trailing spaces
    reply = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', reply)       # remove non‑printable chars
    # Capitalise first alphabetic character
    for i, c in enumerate(reply):
        if c.isalpha():
            reply = reply[:i] + c.upper() + reply[i+1:]
            break
    # Ensure a sentence‑ending punctuation
    if reply and reply[-1] not in ".!?":
        reply += "."
    return reply


def generate_reply(history: list) -> str:
    if not history:
        return "Hello! How can I assist you with booking?"

    # Join last 6 turns (like your test script)
    context = " ".join(history[-6:])
    input_text = f"respond: {context}"

    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        max_length=256,
        truncation=True
    )

    with torch.no_grad():
        reply_ids = model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.8,
            do_sample=True,
            no_repeat_ngram_size=3
        )

    reply = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    reply = _clean_and_capitalize(reply)          # <-- NEW line
    return reply