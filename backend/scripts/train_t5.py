# ultra_fast_prototype_FINAL.py  ← THIS ONE ACTUALLY WORKS
import json, os
os.environ["TOKENIZERS_PARALLELISM"] = "false"   # Prevents deadlocks
# DO NOT set CUDA_VISIBLE_DEVICES here — let PyTorch auto-detect

from datasets import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
import torch

print("Loading data (max 8000 examples for speed)...")

data = []
count = 0
with open("C:/Users/Awoleye/ecom_chatbot/data/final_training_data.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if count >= 8000:
            break
        obj = json.loads(line.strip())
        turns = obj["turns"]
        context = []
        for t in turns:
            text = t["text"].replace("multiwoz:", "").replace("multiwoz :", "").strip()
            if t["speaker"] == "customer":
                context.append(f"User: {text}")
            elif t["speaker"] == "agent" and context:
                # Proper input → real next reply
                data.append({
                    "input": f"respond: {' '.join(context[-6:])}",
                    "target": text
                })
                context.append(f"Bot: {text}")
        count += 1

print(f"Created {len(data)} high-quality training examples")

# Dataset
dataset = Dataset.from_list(data).train_test_split(test_size=0.1, seed=42)

# Model + tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Preprocessing
def preprocess(ex):
    inputs = tokenizer(ex["input"], max_length=256, truncation=True, padding=False)
    targets = tokenizer(ex["target"], max_length=128, truncation=True, padding=False)
    inputs["labels"] = targets["input_ids"]
    return inputs

tokenized = dataset.map(preprocess, batched=True, remove_columns=["input", "target"])

# Training args — THE ONLY ONES THAT WORK ON LAPTOP
args = Seq2SeqTrainingArguments(
    output_dir="model/fast_proto",
    eval_strategy="no",
    save_strategy="no",
    learning_rate=5e-4,
    per_device_train_batch_size=8,        # Safe for CPU + small GPU
    gradient_accumulation_steps=4,        # Makes effective batch = 32
    num_train_epochs=3,
    logging_steps=50,
    fp16=torch.cuda.is_available(),       # Only enable if GPU exists
    bf16=False,
    dataloader_num_workers=0,             # ← MUST be 0 on Windows
    report_to=[],
    disable_tqdm=False,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
    tokenizer=tokenizer,
)

print("Starting training — will finish in 8–15 minutes on your laptop")
trainer.train()

# Save
os.makedirs("model/fast_proto", exist_ok=True)
trainer.save_model("model/fast_proto")
tokenizer.save_pretrained("model/fast_proto")
print("PROTOTYPE READY! Run test_prototype.py now")