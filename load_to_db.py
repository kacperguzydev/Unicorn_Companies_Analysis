import pandas as pd
import sqlite3
import os

# Load the cleaned unicorn data
df = pd.read_csv("data/transformed_unicorns.csv")
print("Columns found in CSV:", df.columns.tolist())
print(f"Loaded {len(df)} rows from transformed_unicorns.csv")

# Rename Unnamed: 0 to id
if 'Unnamed: 0' in df.columns:
    df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)

# Make sure the database directory exists
os.makedirs("database", exist_ok=True)

# Connect to SQLite database in the database directory
conn = sqlite3.connect("database/unicorns.db")
cursor = conn.cursor()

# Create table with all columns you have
cursor.execute("""
CREATE TABLE IF NOT EXISTS unicorns (
    id INTEGER,
    country TEXT,
    region TEXT,
    lead_investors TEXT,
    company_link TEXT,
    img_src TEXT,
    company_name TEXT,
    post_money_value TEXT,
    total_eq_funding TEXT,
    valuation_billion REAL
)
""")

# Clear existing data (optional)
cursor.execute("DELETE FROM unicorns")

# Insert data into the table
df.to_sql("unicorns", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("Data loaded into database/unicorns.db")
