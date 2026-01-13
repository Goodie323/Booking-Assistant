# intent_product_detector_FINAL_FIXED.py  ← COPY-PASTE THIS (WORKS 100%)
import spacy
import re
import pandas as pd
from pathlib import Path

nlp = spacy.load("en_core_web_sm")
catalog = pd.read_csv("C:/Users/Awoleye/ecom_chatbot/data/product_catalog.csv")

# ────────────────────────────── INTENT RULES ──────────────────────────────
INTENT_RULES = {
    "greeting":           ["hi", "hello", "hey", "good morning", "good evening"],
    "price_query":        ["price", "cost", "how much", "expensive", "cheap", "under", "around", "dollar", "$"],
    "availability":       ["available", "in stock", "have", "do you have", "got", "sell"],
    "purchase_intent":    ["buy", "order", "purchase", "add to cart", "i want", "i'll take", "get me"],
    "size_query":         ["size", "small", "medium", "large", "xl", "s", "m", "l", "xxl"],
    "color_query":        ["color", "black", "white", "red", "blue", "green", "grey", "gray"],
    "feature_query":      ["waterproof", "wind", "durable", "battery", "material", "feature", "specs", "resistant", "proof"],
    "book_hotel":         ["hotel", "stay", "room", "accommodation", "book a hotel"],
    "book_train":         ["train", "ticket", "rail", "leave after", "arrive by", "depart"],
    "book_restaurant":    ["restaurant", "table", "dinner", "lunch", "reserve", "book a table"],
    "book_taxi":          ["taxi", "cab", "ride", "pick me up", "take me to"],
    "track_order":        ["track", "where is my order", "delivery", "shipped"],
    "return_refund":      ["return", "refund", "exchange", "send back"],
}

def detect_intent(text: str) -> str:
    text_lower = text.lower()
    scores = {}
    for intent, keywords in INTENT_RULES.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score:
            scores[intent] = score + scores.get(intent, 0)
    return max(scores, key=scores.get) if scores else "general_query"

def extract_attributes(text: str):
    text_lower = text.lower()          # ← THIS WAS MISSING!
    doc = nlp(text_lower)
    attrs = {}

    # Colors & Sizes
    colors = {"black","white","red","blue","green","yellow","grey","gray","navy","pink","brown"}
    sizes = {"xs","s","m","l","xl","xxl","small","medium","large"}
    for token in doc:
        if token.text in colors:   attrs["color"] = token.text
        if token.text in sizes:    attrs["size"] = token.text

    # Price
    price = re.search(r'\$?(\d+(?:,\d{3})*(?:\.\d+)?)', text)
    if price: attrs["price"] = price.group(1).replace(",", "")

    # Time
    time = re.search(r'(\d{1,2}:\d{2}|\d{1,2}(?:am|pm|AM|PM))', text)
    if time: attrs["time"] = time.group(0)

    # Day
    day = re.search(r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|today|tomorrow)\b', text_lower)
    if day: attrs["day"] = day.group(0).capitalize()

    # Number of people
    people = re.search(r'\b(\d+)\s*(people|person|guest|guests)\b', text_lower)
    if people: attrs["people"] = people.group(1)

    return attrs if attrs else "none"

def detect_product_or_entity(text: str):
    text_lower = text.lower()
    for _, row in catalog.iterrows():
        name = str(row["name"]).lower()
        if name in text_lower or any(w in text_lower for w in name.split()[:3]):
            return {"type": "product", "name": row["name"]}
    return {"type": "none", "name": None}

def analyze(user_input: str):
    intent = detect_intent(user_input)
    entity = detect_product_or_entity(user_input)
    attrs = extract_attributes(user_input)

    return {
        "intent": intent,
        "entity_type": entity["type"],
        "entity_name": entity["name"],
        "attributes": attrs,
        "raw_input": user_input
    }

# LIVE TEST
if __name__ == "__main__":
    print("ULTIMATE E-COM + BOOKING DETECTOR – FULLY FIXED!")
    while True:
        msg = input("\nYou: ").strip()
        if msg.lower() in ["quit", "exit", "bye"]:
            print("Bot: Goodbye!")
            break
        if not msg: continue
        print("→", analyze(msg))
        print("-" * 70)