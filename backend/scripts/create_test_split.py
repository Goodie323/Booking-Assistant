import json
import random
import os

# Paths
data_path = "C:/Users/Awoleye/ecom_chatbot/data/final_training_data.jsonl"
train_output = "C:/Users/Awoleye/ecom_chatbot/data/hybrid_dialogues_train.json"
test_output = "C:/Users/Awoleye/ecom_chatbot/data/hybrid_dialogues_test.json"

# Ensure reproducibility
random.seed(42)

def create_test_split():
    # Load JSONL dataset (one JSON object per line)
    dataset = []
    with open(data_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            try:
                dataset.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON on line {line_num}: {e}")
                continue
    
    print(f"Successfully loaded {len(dataset)} valid samples from {data_path}")

    if len(dataset) == 0:
        print("Error: No valid data loaded!")
        return

    # Shuffle dataset
    random.shuffle(dataset)

    # 90% train, 10% test
    split_idx = int(0.9 * len(dataset))
    train_data = dataset[:split_idx]
    test_data = dataset[split_idx:]

    # Save outputs as proper JSON arrays
    with open(train_output, "w", encoding="utf-8") as f:
        json.dump(train_data, f, indent=2, ensure_ascii=False)

    with open(test_output, "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*50}")
    print(f"TRAIN/TEST SPLIT COMPLETED")
    print(f"{'='*50}")
    print(f"Total samples: {len(dataset):,}")
    print(f"Training samples: {len(train_data):,} ({len(train_data)/len(dataset)*100:.1f}%)")
    print(f"Test samples: {len(test_data):,} ({len(test_data)/len(dataset)*100:.1f}%)")
    print(f"{'='*50}")
    print(f"✅ Train dataset saved to: {train_output}")
    print(f"✅ Test dataset saved to: {test_output}")

if __name__ == "__main__":
    create_test_split()