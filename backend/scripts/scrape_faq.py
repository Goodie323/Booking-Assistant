import requests
import pandas as pd
import os
from bs4 import BeautifulSoup

# Simple, reliable outdoor gear site
url = "https://www.rei.com/learn/expert-advice"

print("Fetching outdoor advice from REI...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    print(f"Success! Status: {response.status_code}")
except Exception as e:
    print(f"Fetch failed: {e}")
    # Fallback to creating sample data
    print("Creating sample FAQ data instead...")
    faqs = [
        {"question": "What should I wear for hiking?", "answer": "Wear moisture-wicking layers and proper hiking boots for comfort and safety.", "source_url": "sample"},
        {"question": "How do I choose a sleeping bag?", "answer": "Consider temperature rating, insulation type, and weight based on your camping needs.", "source_url": "sample"},
        {"question": "What essentials should I pack for a day hike?", "answer": "Bring water, snacks, navigation, first aid, and emergency supplies.", "source_url": "sample"}
    ]
    df = pd.DataFrame(faqs)
    os.makedirs("data/scraped_data", exist_ok=True)
    df.to_csv("data/scraped_data/simple_faq.csv", index=False)
    print("Sample FAQs created!")
    exit(0)

soup = BeautifulSoup(response.text, "html.parser")

faqs = []

# Simple parsing - look for headings and following paragraphs
headings = soup.find_all(['h2', 'h3', 'h4'])[:10]  # First 10 headings

for heading in headings:
    question = heading.get_text(strip=True)
    if len(question) > 10:
        # Get next paragraph as answer
        next_p = heading.find_next('p')
        answer = next_p.get_text(strip=True)[:150] + "..." if next_p else "Learn more on our website"
        
        faqs.append({
            "question": question,
            "answer": answer,
            "source_url": url
        })

df = pd.DataFrame(faqs)
os.makedirs("data/scraped_data", exist_ok=True)
df.to_csv("data/scraped_data/simple_faq.csv", index=False)

print(f"Done! {len(df)} FAQs saved to data/scraped_data/simple_faq.csv")