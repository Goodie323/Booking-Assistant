import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
PROJECT_ID = os.getenv("OPENAI_PROJECT_ID")  # Optional

print("🔍 DEBUG INFO:")
print(f"API_KEY loaded: {'✅ YES' if API_KEY else '❌ NO'} ({API_KEY[:15]}...)" if API_KEY else "❌ NO API_KEY")
print(f"PROJECT_ID loaded: {'✅ YES' if PROJECT_ID else '❌ OPTIONAL'} ({PROJECT_ID})")

if not API_KEY:
    print("\n💥 FIX: Add OPENAI_API_KEY to .env")
    exit(1)

# Initialize client
client = OpenAI(
    api_key=API_KEY,
    # Optional: Explicitly set project (SDK uses it if provided)
    project=PROJECT_ID
)

print(f"\n📤 Sending to OpenAI...")

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Fixed: "gpt-4.1-mini" → "gpt-4o-mini" (valid model)
        messages=[{"role": "user", "content": "Say 'API WORKS!'"}],
        max_tokens=10
    )
    
    content = response.choices[0].message.content
    print(f"\n🎉 SUCCESS! OpenAI says: '{content}'")
    print(f"Full response: {json.dumps(response.model_dump(), indent=2)[:300]}...")
    
except Exception as e:
    print(f"\n💥 Error: {e}")
    if "401" in str(e):
        print("🔄 Likely: Key revoked or project mismatch. Create a fresh sk-proj- key and match PROJECT_ID exactly.")
    elif "model" in str(e).lower():
        print("🔄 Model name typo? Use 'gpt-4o-mini' instead.")

print("\n" + "="*50)
print("NEXT STEPS: If success, run the full synthetic script below!")