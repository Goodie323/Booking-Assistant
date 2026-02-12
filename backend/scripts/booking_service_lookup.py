import pandas as pd

# Load service catalog
catalog = pd.read_csv("C:/Users/Awoleye/ecom_chatbot/backend/data/service_catalog.csv")

def find_by_name(name):
    name = name.lower()
    for _, row in catalog.iterrows():
        if row["name"].lower() in name or name in row["name"].lower():
            return row.to_dict()
    return None

def filter_services(service_type=None, area=None, cuisine=None, price_range=None, stars=None):
    df = catalog.copy()

    if service_type:
        df = df[df['type'].str.lower() == service_type.lower()]
    
    if area:
        df = df[df['area'].str.lower() == area.lower()]
    
    if cuisine:
        df = df[df['cuisine'].str.lower() == cuisine.lower()]
    
    if price_range:
        df = df[df['price_range'].str.lower() == price_range.lower()]
    
    if stars:
        df = df[df['stars'].astype(str).str.lower() == str(stars).lower()]

    if df.empty:
        return []
    
    return df.to_dict(orient="records")

def suggest_services(service_type, area=None):
    df = catalog[catalog['type'].str.lower() == service_type.lower()]
    if area:
        df = df[df['area'].str.lower() == area.lower()]
    return df.to_dict(orient="records")

if __name__ == "__main__":
    print("\nTest: Indian restaurant in the center")
    results = filter_services(service_type="Restaurant", area="center", cuisine="Indian")
    print(results)

    print("\nTest: 3-star hotel with moderate price")
    results = filter_services(service_type="Hotel", stars=3, price_range="moderate")
    print(results)
