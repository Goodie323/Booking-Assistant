# scripts/generate_synthetic.py
import os
import json
import pandas as pd
import time
import requests
import random
from dotenv import load_dotenv

load_dotenv()  # ← loads .env automatically

API_KEY = os.getenv("OPENAI_API_KEY")
PROJECT_ID = os.getenv("OPENAI_PROJECT_ID")   # ← this is the crucial new line

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")
if not PROJECT_ID:
    raise ValueError("OPENAI_PROJECT_ID not found in .env – copy it from https://platform.openai.com/api-keys")

API_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "OpenAI-Project": PROJECT_ID          # ← this fixes the 401
}

def build_prompt(product):
    return f"""
You are an intelligent e-commerce support agent.
Your task: generate realistic customer–agent dialogues grounded ONLY in the product information provided below.

PRODUCT FACTS:
Name: {product['name']}
Category: {product['category']}
Material: {product['material']}
Features: {product['features']}
Use-case: {product['use_case']}
Price: ${product['price']}
Description: {product['description']}

RULES:
- Do NOT add any information not provided above.
- Do NOT hallucinate features or materials.
- The agent must ONLY use facts from the product catalog.
- Dialogue must be exactly 4 turns: customer → agent → customer → agent.
- Make it sound natural and context-aware.

OUTPUT FORMAT (STRICT JSON only, no extra text):
{{
  "dialogue": [
     {{"speaker": "customer", "text": "..."}},
     {{"speaker": "agent", "text": "..."}},
     {{"speaker": "customer", "text": "..."}},
     {{"speaker": "agent", "text": "..."}}
  ]
}}
"""

def generate_dialogue(prompt, retries=8):
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.7
    }

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            if response.status_code == 429:
                wait = (2 ** attempt) + random.random()
                print(f"   Rate limited. Waiting {wait:.1f}s...")
                time.sleep(wait)
                continue
            response.raise_for_status()
            raw = response.json()["choices"][0]["message"]["content"]
            return raw
        except Exception as e:
            print(f"   Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return None

def main():
    df = pd.read_csv("data/product_catalog.csv")
    results = []
    os.makedirs("data/synthetic_data", exist_ok=True)

    total = len(df) * 5
    current = 0

    for _, product in df.iterrows():
        for i in range(5):
            current += 1
            print(f"[{current}/{total}] Generating dialogue for {product['name']} #{i+1}...", end="")

            prompt = build_prompt(product.to_dict())
            output = generate_dialogue(prompt)

            if output:
                # Clean common leading/trailing markdown
                cleaned = output.strip().strip("```json").strip("```")
                try:
                    data = json.loads(cleaned)
                    print(" ✓")
                except json.JSONDecodeError:
                    data = {"raw_output": output, "error": "JSON parse failed"}
                    print(" JSON failed")
            else:
                data = {"error": "API call failed"}
                print(" API failed")

            results.append({
                "product_id": product.get("product_id", product["name"]),
                "dialogue_id": f"{product.get('product_id', product['name'])}_{i+1}",
                "dialogue": data
            })

            # Save progressively
            with open("data/synthetic_data/synthetic_dialogues.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            time.sleep(1.5)  # be gentle

    print("\nALL DONE! Generated", len(results), "dialogues.")
    print("Saved to data/synthetic_data/synthetic_dialogues.json")

if __name__ == "__main__":
    main()