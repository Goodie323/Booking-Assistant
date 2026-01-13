import json
import math
from transformers import T5Tokenizer, T5ForConditionalGeneration
import evaluate

# Load model and tokenizer
model_path = "C:/Users/Awoleye/ecom_chatbot/model/my_final_model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Load test dataset
test_file = "C:/Users/Awoleye/ecom_chatbot/data/hybrid_dialogues_test.json"

with open(test_file, "r") as f:
    test_data = json.load(f)

# BLEU metric
bleu = evaluate.load("bleu")

def prepare_conversation_pairs(dialogues):
    """Convert dialogue turns into input-target pairs for evaluation"""
    pairs = []
    
    for dialogue in dialogues:
        turns = dialogue["turns"]
        
        # Create conversation history for each turn
        for i in range(1, len(turns)):
            if turns[i]["speaker"] == "agent":  # We want to predict agent responses
                # Previous turns as context
                context = " ".join([turn["text"] for turn in turns[:i]])
                target = turns[i]["text"]
                
                pairs.append({
                    "input": context,
                    "target": target
                })
    
    return pairs

def calculate_bleu_and_perplexity():
    # Prepare the data in input-target format
    test_pairs = prepare_conversation_pairs(test_data)
    
    references = []
    predictions = []
    total_loss = 0.0
    total_tokens = 0

    print(f"\nEvaluating model on {len(test_pairs)} conversation pairs...")

    for i, sample in enumerate(test_pairs):
        input_text = sample["input"]
        target_text = sample["target"]

        # Tokenize
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
        labels = tokenizer(target_text, return_tensors="pt", truncation=True, max_length=512)

        # Forward pass for loss (perplexity)
        output = model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            labels=labels["input_ids"]
        )

        loss = output.loss
        total_loss += loss.item()
        total_tokens += labels["input_ids"].numel()

        # Generate prediction for BLEU
        generated = model.generate(
            **inputs, 
            max_new_tokens=80,
            num_beams=5,
            early_stopping=True,
            no_repeat_ngram_size=2
        )
        decoded = tokenizer.decode(generated[0], skip_special_tokens=True)

        predictions.append(decoded.split())
        references.append([target_text.split()])

        # Print progress
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{len(test_pairs)} samples")

    # Compute BLEU
    bleu_score = bleu.compute(predictions=predictions, references=references)["bleu"]

    # Compute perplexity
    perplexity = math.exp(total_loss / len(test_pairs))

    return bleu_score, perplexity, test_pairs

if __name__ == "__main__":
    bleu_score, perplexity, test_pairs = calculate_bleu_and_perplexity()

    print("\n=== Evaluation Results ===")
    print(f"Number of test pairs: {len(test_pairs)}")
    print(f"BLEU Score: {bleu_score:.4f}")
    print(f"Perplexity: {perplexity:.4f}\n")
    
    # Print a few examples for verification
    print("=== Sample Predictions ===")
    for i in range(min(3, len(test_pairs))):
        print(f"\nExample {i+1}:")
        print(f"Input: {test_pairs[i]['input'][:100]}...")
        print(f"Target: {test_pairs[i]['target']}")
        print(f"Predicted: {tokenizer.decode(model.generate(**tokenizer(test_pairs[i]['input'], return_tensors='pt', truncation=True, max_length=512), max_new_tokens=80, num_beams=5)[0], skip_special_tokens=True)}")