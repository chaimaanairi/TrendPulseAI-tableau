"""
TrendPredict – AI-Powered Recommendations (Dynamic)
Author: Chaimaa Nairi
Description:
Reads existing Twitter/X data CSV (with momentum and sentiment_vader)
and generates AI-powered recommendations based on trend momentum and sentiment.
Uses percentiles to scale momentum and ensure diverse recommendations.
Adds a new column: ai_recommendation for Tableau dashboards.
"""

import pandas as pd

# -------------------------
# Configuration
# -------------------------
CSV_INPUT = "../data/twitter_trends_vader.csv"  # CSV with sentiment_vader
CSV_OUTPUT = "../data/twitter_trends_ai.csv"

# -------------------------
# Load CSV
# -------------------------
df = pd.read_csv(CSV_INPUT)

# -------------------------
# Compute momentum percentile
# -------------------------
df["momentum_pct"] = df["momentum"].rank(pct=True)

# -------------------------
# Recommendation function
# -------------------------
def recommendation(row):
    momentum_pct = row["momentum_pct"]
    sentiment = row["sentiment_vader"]

    if momentum_pct > 0.75 and sentiment > 0.3:
        return "Launch marketing campaign now"
    elif momentum_pct > 0.5:
        return "Monitor closely – trend emerging"
    elif sentiment < -0.1:
        return "Reputation risk – investigate"
    else:
        return "No action needed"

# -------------------------
# Apply recommendations
# -------------------------
df["ai_recommendation"] = df.apply(recommendation, axis=1)

# -------------------------
# Save output CSV
# -------------------------
df.to_csv(CSV_OUTPUT, index=False, encoding="utf-8")
print(f"✅ AI recommendations added → {CSV_OUTPUT} ({len(df)} rows)")