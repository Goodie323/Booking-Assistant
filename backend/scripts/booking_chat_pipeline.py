from transformers import T5Tokenizer, T5ForConditionalGeneration    
import random
import string
from .booking_matcher import find_matches
from .booking_intent_detector import is_booking_confirmation


# Load trained model
# model_path = "C:/Users/Awoleye/ecom_chatbot/model/my_final_model"
# tokenizer = T5Tokenizer.from_pretrained(model_path)
# model = T5ForConditionalGeneration.from_pretrained(model_path)

from transformers import T5Tokenizer, T5ForConditionalGeneration

HF_MODEL_ID = "SmartBott/my_final_model"

tokenizer = T5Tokenizer.from_pretrained(HF_MODEL_ID)
model = T5ForConditionalGeneration.from_pretrained(HF_MODEL_ID)



def generate_reference():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def build_context(user_message, matches):
    results = matches["results"]

    # No matches found
    if len(results) == 0:
        return f"""
User: {user_message}
Assistant role: Booking assistant.
Instruction: No matching services were found. Ask a helpful follow-up question to narrow down options.
"""

    # One match found
    if len(results) == 1:
        service = results[0]
        return f"""
User: {user_message}

Service details:
Name: {service.get('name')}
Type: {service.get('type')}
Area: {service.get('area')}
Cuisine: {service.get('cuisine')}
Stars: {service.get('stars')}
Price: {service.get('price_range')}
Capacity: {service.get('capacity')}
Policies: {service.get('policies')}
Description: {service.get('description')}

Instruction:
Give a helpful, accurate response about this service. 
Offer to help with booking. 
Do NOT invent details.
"""

    # Multiple matches found
    names = [s.get('name') for s in results]
    name_list = ", ".join(names)
    return f"""
User: {user_message}

Matching options:
{name_list}

Instruction:
Inform the user how many options match their request and list them.
Ask a helpful follow-up question (e.g., price range, area, time).
Do NOT make up details.
"""

def chat(user_message):
    # ✅ Booking confirmation check FIRST
    if is_booking_confirmation(user_message):
        ref = generate_reference()
        return f"✅ Your reservation is confirmed! Your reference number is {ref}. You're all set."

    # ✅ Normal flow
    matches = find_matches(user_message)
    prompt = build_context(user_message, matches)

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=80)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return reply

if __name__ == "__main__":
    print("\n✅ Booking Assistant Ready\n")
    while True:
        user_input = input("You: ")
        response = chat(user_input)
        print("Bot:", response, "\n")
