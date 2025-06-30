import pandas as pd
import re

# Load the unicorn data from CSV
df = pd.read_csv("data/unicorn_companies.csv")
print("Columns found in CSV:", df.columns.tolist())

# Clean up post_money_value (convert strings like '$1.2B' or '$500M' to numeric billions)
def parse_valuation(val):
    if pd.isna(val):
        return None
    val = str(val).replace('$', '').replace(',', '').strip()
    match = re.match(r"([0-9.]+)([MB]?)", val, re.IGNORECASE)
    if not match:
        return None
    num, suffix = match.groups()
    num = float(num)
    if suffix.upper() == 'M':
        return num / 1000  # Convert millions to billions
    elif suffix.upper() == 'B':
        return num
    else:
        return num  # assume billions if no suffix

df['valuation_billion'] = df['post_money_value'].apply(parse_valuation)

# Drop rows with missing company_name or valuation
df.dropna(subset=['company_name', 'valuation_billion'], inplace=True)

# Clean up company names and country
df['company_name'] = df['company_name'].str.strip()
df['country'] = df['country'].str.strip()

# Save the cleaned data
df.to_csv("data/transformed_unicorns.csv", index=False)

print(f"Transformation complete. Saved {len(df)} rows to data/transformed_unicorns.csv.")
