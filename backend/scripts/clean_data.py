# clean_data.py  (Run this first!)
import json

input_path = "C:/Users/Awoleye/ecom_chatbot/data/final_training_data.jsonl"
output_path = "C:/Users/Awoleye/ecom_chatbot/data/cleaned_training_data.jsonl"

with open(input_path, "r", encoding="utf-8") as fin, \
     open(output_path, "w", encoding="utf-8") as fout:

    for line in fin:
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        turns = obj["turns"]

        # Remove "multiwoz: " prefix and clean
        cleaned_turns = []
        for turn in turns:
            text = turn["text"]
            if text.startswith("multiwoz:"):
                text = text[len("multiwoz:"):].strip()
            cleaned_turns.append({
                "speaker": turn["speaker"],
                "text": text
            })
        obj["turns"] = cleaned_turns
        fout.write(json.dumps(obj, ensure_ascii=False) + "\n")

print("Cleaned data saved to:", output_path)