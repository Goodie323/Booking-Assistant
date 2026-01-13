# test_chatbot.py  ← RUN THIS
from transformers import T5Tokenizer, T5ForConditionalGeneration

print("Loading your AI assistant...")
tokenizer = T5Tokenizer.from_pretrained("C:/Users/Awoleye/ecom_chatbot/model/my_final_model", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("C:/Users/Awoleye/ecom_chatbot/model/my_final_model")
model.eval()

print("Chatbot ready! Type 'bye' to quit\n")

history = []
while True:
    user = input("You: ").strip()
    if user.lower() in ["bye", "quit", "exit"]:
        print("Bot: Goodbye!")
        break
    if not user:
        continue

    history.append(f"User: {user}")
    input_text = f"respond: {' '.join(history[-6:])}"

    inputs = tokenizer(input_text, return_tensors="pt", max_length=256, truncation=True)
    reply_ids = model.generate(
        **inputs,
        max_new_tokens=100,
        temperature=0.8,
        do_sample=True,
        no_repeat_ngram_size=3
    )
    reply = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    print(f"Bot: {reply}\n")
    history.append(f"Bot: {reply}")