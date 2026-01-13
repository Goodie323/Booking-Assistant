# debug_data_sources.py
from pathlib import Path
import pandas as pd

def check_data_sources():
    print("=== CHECKING DATA SOURCES ===\n")
    
    # Check synthetic data
    synthetic_path = Path("data/synthetic_data/synthetic_dialogues.json")
    print(f"1. Synthetic data: {synthetic_path}")
    print(f"   Exists: {synthetic_path.exists()}")
    if synthetic_path.exists():
        with open(synthetic_path, 'r') as f:
            import json
            data = json.load(f)
            print(f"   Dialogues: {len(data)}")
    
    # Check scraped data
    scraped_path = Path("data/scraped_data/faq_pairs.csv")
    print(f"\n2. Scraped data: {scraped_path}")
    print(f"   Exists: {scraped_path.exists()}")
    if scraped_path.exists():
        try:
            df = pd.read_csv(scraped_path)
            print(f"   Rows: {len(df)}")
            print(f"   Columns: {list(df.columns)}")
            if len(df) > 0:
                print(f"   Sample question: {df.iloc[0]['question']}")
        except Exception as e:
            print(f"   Error reading CSV: {e}")
    
    # Check MultiWOZ data
    multiwoz_path = Path("data/base_dataset/multiwoz_train")
    print(f"\n3. MultiWOZ data: {multiwoz_path}")
    print(f"   Exists: {multiwoz_path.exists()}")
    
    if multiwoz_path.exists():
        try:
            from datasets import load_from_disk
            dataset = load_from_disk(str(multiwoz_path))
            print(f"   Dataset loaded: {len(dataset)} examples")
            if len(dataset) > 0:
                sample = dataset[0]
                print(f"   Sample keys: {list(sample.keys())}")
        except Exception as e:
            print(f"   Error loading MultiWOZ: {e}")
    else:
        # Check for MultiWOZ in common alternative locations
        alternatives = [
            Path("data/base_dataset/multiwoz"),
            Path("data/multiwoz"),
            Path("multiwoz_train"),
            Path("data/base_dataset"),
        ]
        print("   Checking alternative locations:")
        for alt in alternatives:
            if alt.exists():
                print(f"     Found: {alt}")

check_data_sources()