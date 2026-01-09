"""
TrendPredict – JSON to CSV Converter
Author: Chaimaa Nairi
Description:
Reads the Twitter/X JSON data and outputs a CSV file compatible
with the Tableau dashboard.
"""

import json
import pandas as pd
import os

# -------------------------
# Config
# -------------------------
JSON_FILE = "../data/twitter_trends.json"
CSV_FILE = "../data/twitter_trends.csv"

# -------------------------
# Load JSON
# -------------------------
if not os.path.exists(JSON_FILE):
    raise FileNotFoundError(f"❌ JSON file not found: {JSON_FILE}")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# -------------------------
# Convert to DataFrame
# -------------------------
df = pd.DataFrame(data)

# -------------------------
# Ensure all expected columns exist
# -------------------------
expected_columns = [
    "tweet_id",
    "created_at",
    "text",
    "likes",
    "retweets",
    "sentiment",
    "sentiment_category",
    "hashtag",
    "momentum",
    "momentum_status",
    "user_location"
]

for col in expected_columns:
    if col not in df.columns:
        df[col] = None  # add missing columns as empty

# Reorder columns
df = df[expected_columns]

# -------------------------
# Save CSV
# -------------------------
df.to_csv(CSV_FILE, index=False, encoding="utf-8")
print(f"✅ CSV created from JSON → {CSV_FILE} ({len(df)} rows)")