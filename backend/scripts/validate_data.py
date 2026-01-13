import json

count = 0
with open("C:/3Users/Awoleye/ecom_chatbot/data/final_training_data.jsonl", "r") as f:
    for line in f:
        obj = json.loads(line)
        assert len(obj["turns"]) >= 2, "A dialogue has less than 2 turns!"
        count += 1

print("All good! Total dialogues:", count)
