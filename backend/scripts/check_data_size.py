# check_data_size.py
import json
count = 0
with open("C:/Users/Awoleye/ecom_chatbot/data/final_training_data.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            count += 1
print(f"Your model was trained on {count} dialogues")