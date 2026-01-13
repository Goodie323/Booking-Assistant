import re

SERVICE_TYPES = {
    "restaurant": ["restaurant", "place to eat", "dining"],
    "hotel": ["hotel", "guesthouse", "guest house"],
    "train": ["train"]
}

AREAS = ["center", "west", "east", "north", "south"]

CUISINES = ["indian", "chinese", "italian", "british", "french"]  # Can expand later

PRICE_RANGES = {
    "cheap": ["cheap", "affordable", "low price", "budget"],
    "moderate": ["moderate", "mid range"],
    "expensive": ["expensive", "high end", "pricey"]
}

def extract_service_type(text):
    text = text.lower()
    for stype, keywords in SERVICE_TYPES.items():
        if any(kw in text for kw in keywords):
            return stype
    return None

def extract_area(text):
    text = text.lower()
    for area in AREAS:
        if area in text:
            return area
    return None

def extract_cuisine(text):
    text = text.lower()
    for cuisine in CUISINES:
        if cuisine in text:
            return cuisine
    return None

def extract_price_range(text):
    text = text.lower()
    for prange, keywords in PRICE_RANGES.items():
        if any(kw in text for kw in keywords):
            return prange
    return None

def extract_stars(text):
    match = re.search(r"(\d)\s*star", text.lower())
    if match:
        return match.group(1)
    return None

def extract_attributes(text):
    return {
        "service_type": extract_service_type(text),
        "area": extract_area(text),
        "cuisine": extract_cuisine(text),
        "price_range": extract_price_range(text),
        "stars": extract_stars(text)
    }

if __name__ == "__main__":
    while True:
        user = input("\nUser: ")
        print(extract_attributes(user))
