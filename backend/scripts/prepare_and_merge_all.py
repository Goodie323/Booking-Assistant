# 1_prepare_and_merge_all.py  ← FINAL VERSION: USES EVERYTHING (no limits)
import json
import pandas as pd
from pathlib import Path
from datasets import Dataset

print("Loading and merging ALL your data — no limits, no pegging!\n")

# === 1. MultiWOZ 2.1 (full) ===
raw_path = Path("C:/Users/Awoleye/ecom_chatbot/data/multiwoz/MultiWOZ_2.1/data.json")
if not raw_path.exists():
    raise FileNotFoundError(f"MultiWOZ file not found at {raw_path}")

print("Loading full MultiWOZ 2.1 data.json...")
with open(raw_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

dialogues = []
for dial_id, dial in raw_data.items():
    turns = []
    for turn in dial["log"]:
        text = turn.get("text", "").strip()
        if not text:
            continue
        speaker = "agent" if turn.get("metadata") else "customer"
        turns.append({"speaker": speaker, "text": text})

    if len(turns) >= 2:
        # Add prefix only to first user turn
        turns[0]["text"] = "multiwoz: " + turns[0]["text"]
        dialogues.append({
            "dialogue_id": dial_id,
            "turns": turns,
            "source": "multiwoz"
        })

print(f"MultiWOZ dialogues loaded: {len(dialogues)} (full dataset used)")

# === 2. Your synthetic e-commerce dialogues ===
syn_data = []
syn_path = Path("C:/Users/Awoleye/ecom_chatbot/data/synthetic_data/synthetic_dialogues.json")
if syn_path.exists():
    print("Loading synthetic e-commerce dialogues...")
    with open(syn_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    for item in raw:
        turns = item.get("dialogue", {}).get("dialogue", [])
        if len(turns) >= 2:
            turns = turns.copy()
            turns[0]["text"] = "ecom: " + turns[0]["text"]
            syn_data.append({
                "dialogue_id": f"syn_{item.get('dialogue_id','')}",
                "turns": turns,
                "source": "synthetic_ecom"
            })
print(f"Synthetic e-com dialogues: {len(syn_data)}")

# === 3. Your scraped FAQ / simple Q&A ===
faq_data = []
faq_path = Path("C:/Users/Awoleye/ecom_chatbot/data/scraped_data/simple_faq.csv")
if faq_path.exists():
    print("Loading FAQ data...")
    df = pd.read_csv(faq_path)
    for i, row in df.iterrows():
        q = str(row.get("question", "")).strip()
        a = str(row.get("answer", "")).strip()
        if q and a:
            faq_data.append({
                "dialogue_id": f"faq_{i}",
                "turns": [
                    {"speaker": "customer", "text": f"ecom: {q}"},
                    {"speaker": "agent",   "text": a}
                ],
                "source": "scraped_ecom"
            })
print(f"FAQ entries converted: {len(faq_data)}")

# === FINAL MERGE: EVERYTHING ===
final_data = syn_data + faq_data + dialogues   # ← NO slicing, NO 1500 limit

print("\n" + "="*50)
print(f"Synthetic e-com   : {len(syn_data)}")
print(f"FAQ e-com         : {len(faq_data)}")
print(f"Full MultiWOZ     : {len(dialogues)}")
print(f"TOTAL DIALOGUES   : {len(final_data)}  ← THIS IS WHAT YOUR MODEL WILL SEE")
print("="*50)

# Save
output_file = Path("C:/Users/Awoleye/ecom_chatbot/data/final_training_data.jsonl")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    for item in final_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"\nSUCCESS! Full training file saved:")
print(f"→ {output_file}")
print(f"Size: {output_file.stat().st_size / (1024*1024):.1f} MB")
print("\nNow go train with this file — your bot will be WAY smarter!")