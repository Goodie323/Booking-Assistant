import pandas as pd
import psycopg2
from io import StringIO

df = pd.read_csv("data/product_catalog.csv")

# Fix column names for PostgreSQL
df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]

# Connection (NO URI string!)
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="ecomdb",
    user="postgres",
    password="1234"
)
cur = conn.cursor()

# Drop and recreate table
cur.execute("DROP TABLE IF EXISTS products")
# Let pandas infer the SQL types automatically:
sql_table = pd.io.sql.get_schema(df, 'products', con=conn).replace('"', '') + ";"
cur.execute(sql_table)

# Fast upload using COPY
output = StringIO()
df.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
cur.copy_expert("COPY products FROM STDIN WITH (FORMAT CSV, DELIMITER '\t', NULL '')", output)

conn.commit()
cur.close()
conn.close()

print("Uploaded successfully WITHOUT SQLAlchemy!")
print("Total products:", len(df))