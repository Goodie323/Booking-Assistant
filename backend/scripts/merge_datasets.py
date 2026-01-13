import json
import pandas as pd
from pathlib import Path
from datasets import load_from_disk

OUTPUT_FILE = "data/final_training_data.jsonl"

def load_synthetic():
    path = Path("data/synthetic_data/synthetic_dialogues.json")
    if not path.exists():
        return []
    with open(path, "r") as f:
        data = json.load(f)

    final = []
    for item in data:
        dialogue = item.get("dialogue", {})
        final.append({
            "dialogue_id": f"syn_{item['dialogue_id']}",
            "source": "synthetic",
            "product_id": item.get("product_id"),
            "turns": dialogue.get("dialogue", []),
        })
    return final

def load_scraped():
    path = Path("data/scraped_data/faq_pairs.csv")
    if not path.exists():
        return []

    df = pd.read_csv(path)
    final = []
    for i, row in df.iterrows():
        final.append({
            "dialogue_id": f"faq_{i}",
            "source": "scraped",
            "product_id": None,
            "turns": [
                {"speaker": "customer", "text": str(row["question"])},
                {"speaker": "agent", "text": str(row["answer"])}
            ]
        })
    return final

def load_multiwoz():
    path = Path("data/base_dataset/multiwoz_train")
    if not path.exists():
        return []

    dataset = load_from_disk(str(path))
    final = []
    for i, sample in enumerate(dataset):
        turns = []
        for t in sample["dialogue"]:
            speaker = "customer" if t["role"] == "user" else "agent"
            turns.append({"speaker": speaker, "text": t["text"]})
        final.append({
            "dialogue_id": f"mwz_{i}",
            "source": "multiwoz",
            "product_id": None,
            "turns": turns
        })
        if i >= 200:  # limit to first 200 for now
            break
    return final

def save_jsonl(data, out_file):
    with open(out_file, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")

def main():
    print("Loading datasets...")

    syn = load_synthetic()
    print("Synthetic:", len(syn))

    scraped = load_scraped()
    print("Scraped:", len(scraped))

    mwz = load_multiwoz()
    print("MultiWOZ:", len(mwz))

    combined = syn + scraped + mwz
    print("Total merged:", len(combined))

    save_jsonl(combined, OUTPUT_FILE)
    print(f"Saved merged dataset to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
