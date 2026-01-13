# chat_pipeline.py ← YOUR CODE, NOW FIXED & WORKING PERFECTLY
from transformers import T5Tokenizer, T5ForConditionalGeneration
from intent_product_detector import analyze
from db_lookup import fetch_product

# Load model + tokenizer
model_path = "C:/Users/Awoleye/ecom_chatbot/model/my_final_model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

def build_context(product_info, user_message):
    # FIX 1: Correctly check if product_info is None or empty DataFrame
    if product_info is None or product_info.empty:
        return f"User question: {user_message}\nRespond politely and concisely. No matching product found."

    # FIX 2: Use .iloc[0] to get the first row as a Series, then .get() works
    row = product_info.iloc[0]

    context = f"""
Product Name: {row.get('name', 'N/A')}
Category: {row.get('category', 'N/A')}
Material: {row.get('material', 'N/A')}
Features: {row.get('features', 'N/A')}
Use-case: {row.get('use_case', 'N/A')}
Price: ${row.get('price', 'N/A')}
Description: {row.get('description', 'N/A')}

User question: {user_message}

Using ONLY the product details above, give an accurate, friendly answer.
Do NOT guess or invent information.
"""
    return context.strip()

def chat(user_message):
    analysis = analyze(user_message)
    product_name = analysis.get("product")
    product_info = None

    if product_name:
        product_info = fetch_product(product_name)  # Returns DataFrame or empty

    prompt = build_context(product_info, user_message)

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        temperature=0.7,
        do_sample=True,
        top_p=0.9
    )
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    return {
        "intent": analysis.get("intent"),
        "product": product_name,
        "product_info_found": product_info is not None and not product_info.empty,
        "response": reply
    }

if __name__ == "__main__":
    print("E-commerce AI Chatbot Ready! (type 'quit' to exit)\n")
    while True:
        user_msg = input("User: ").strip()
        if user_msg.lower() in ["quit", "exit", "bye", "q"]:
            print("Bot: Goodbye!")
            break
        if not user_msg:
            continue

        result = chat(user_msg)
        print("\nBot:", result["response"])
        print(f"Intent: {result['intent']} | Product: {result['product'] or 'None'} | Found: {result['product_info_found']}")
        print("-" * 80)