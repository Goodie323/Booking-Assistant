# db_lookup.py  ← YOUR ORIGINAL CODE + JUST THIS FIX
import pandas as pd
import psycopg2

# Same connection style as your upload script
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="ecomdb",
    user="postgres",
    password="1234"
)

def fetch_product(search_term):
    query = """
        SELECT 
            product_id,
            name,
            category,
            price,
            material,
            features,
            description,
            image_url
        FROM products 
        WHERE 
            name ILIKE %s
            OR category ILIKE %s
            OR material ILIKE %s
            OR features ILIKE %s
        LIMIT 15
    """
    pattern = f"%{search_term}%"
    
    df = pd.read_sql(query, con=conn, params=(pattern, pattern, pattern, pattern))
    return df

# ← ONLY THIS PART CHANGED (your code stays 99% same)
import atexit
atexit.register(lambda: conn.close() if not conn.closed else None)

if __name__ == "__main__":
    term = input("Enter product name: ").strip()
    if not term:
        print("Nothing entered.")
    else:
        results = fetch_product(term)
        if results.empty:
            print("No products found.")
        else:
            print(f"\nFound {len(results)} matching product(s):\n")
            print(results[['name', 'category', 'price', 'material']].to_string(index=False))
    
    print("\nClosing connection (test mode)...")
    conn.close()