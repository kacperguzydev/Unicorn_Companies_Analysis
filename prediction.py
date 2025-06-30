import sqlite3
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load data from your SQLite database
conn = sqlite3.connect("database/unicorns.db")
query = """
SELECT country, region, valuation_billion
FROM unicorns
WHERE valuation_billion IS NOT NULL
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Drop rows with missing country or region
df.dropna(subset=["country", "region"], inplace=True)

# Features and target
X = df[["country", "region"]]
y = df["valuation_billion"]

# One-hot encode categorical features
X_encoded = pd.get_dummies(X, columns=["country", "region"])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error on test set: {mae:.2f} billion USD")
print(f"R^2 score on test set: {r2:.2f}")

# Save predictions for the whole dataset
df["predicted_valuation"] = model.predict(X_encoded)
os.makedirs("prediction_results", exist_ok=True)
df.to_csv("prediction_results/predicted_company_valuations.csv", index=False)
print("Saved predicted valuations to prediction_results/predicted_company_valuations.csv")
