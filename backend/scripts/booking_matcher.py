from .booking_attribute_extractor import extract_attributes
from .booking_service_lookup import filter_services, find_by_name

def find_matches(user_message):
    attrs = extract_attributes(user_message)

    # If the user explicitly names a place
    direct_match = find_by_name(user_message)
    if direct_match:
        return {
            "match_type": "direct",
            "attributes": attrs,
            "results": [direct_match]
        }

    # Attribute-based lookup
    results = filter_services(
        service_type=attrs.get("service_type"),
        area=attrs.get("area"),
        cuisine=attrs.get("cuisine"),
        price_range=attrs.get("price_range"),
        stars=attrs.get("stars")
    )

    return {
        "match_type": "filtered",
        "attributes": attrs,
        "results": results
    }

if __name__ == "__main__":
    while True:
        msg = input("\nUser: ")
        result = find_matches(msg)
        print("\nExtracted Attributes:", result["attributes"])
        print("Matches Found:", len(result["results"]))
        print("Results:", result["results"])
