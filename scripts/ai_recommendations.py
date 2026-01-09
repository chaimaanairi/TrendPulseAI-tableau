"""
TrendPredict – AI-Powered Recommendations
Author: Chaimaa Nairi
Description:
Reads existing Twitter/X data CSV (with momentum and sentiment_vader) and generates
AI-powered recommendations based on trend momentum and sentiment.
Adds a new column: ai_recommendation for Tableau dashboards.
"""

import pandas as pd

# -------------------------
# Configuration
# -------------------------
CSV_INPUT = "../data/twitter_trends_vader.csv"  # your CSV with sentiment_vader
CSV_OUTPUT = "../data/twitter_trends_ai.csv"

# -------------------------
# Load CSV
# -------------------------
df = pd.read_csv(CSV_INPUT)

# -------------------------
# Check columns (for debugging)
# -------------------------
print("Columns in CSV:", df.columns)

# -------------------------
# Recommendation function
# -------------------------
def recommendation(momentum, sentiment):
    if momentum > 400 and sentiment > 0.3:
        return "🔥 Launch marketing campaign now"
    elif momentum > 250:
        return "🚀 Monitor closely – trend emerging"
    elif sentiment < -0.3:
        return "⚠️ Reputation risk – investigate"
    else:
        return "⏳ No action needed"

# -------------------------
# Apply recommendations
# -------------------------
df["ai_recommendation"] = df.apply(
    lambda row: recommendation(row["momentum"], row["sentiment_vader"]),
    axis=1
)

# -------------------------
# Save output CSV
# -------------------------
df.to_csv(CSV_OUTPUT, index=False, encoding="utf-8")
print(f"✅ AI recommendations added → {CSV_OUTPUT} ({len(df)} rows)")
