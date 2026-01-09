"""
TrendPredict – Twitter/X Feature Engineering
Author: Chaimaa Nairi
Description:
Processes raw Twitter/X data (CSV) and performs feature engineering for Tableau dashboards.
Calculates sentiment categories, momentum scores, engagement metrics, and spike detection.
Generates an enhanced CSV ready for visualization and analytics.
"""

import pandas as pd
import numpy as np
from datetime import datetime

CSV_INPUT = "../data/twitter_trends.csv"
CSV_OUTPUT = "../data/twitter_trends_fe.csv"

# -------------------------
# Load raw CSV
# -------------------------
df = pd.read_csv(CSV_INPUT)

# Ensure datetime format
df["created_at"] = pd.to_datetime(df["created_at"])

# -------------------------
# 1️⃣ Sentiment Category
# -------------------------
def categorize_sentiment(score):
    if score < -0.1:
        return "Negative"
    elif score <= 0.1:
        return "Neutral"
    else:
        return "Positive"

df["sentiment_category"] = df["sentiment"].apply(categorize_sentiment)

# -------------------------
# 2️⃣ Momentum Score
# -------------------------
df["momentum_score"] = round((df["likes"] + df["retweets"]) * 0.7 + df["sentiment"] * 0.3 * 100, 2)

def momentum_status(score):
    if score >= 400:
        return "🔥 Exploding"
    elif score >= 200:
        return "🚀 Emerging"
    else:
        return "⏳ Stable"

df["momentum_status"] = df["momentum_score"].apply(momentum_status)

# -------------------------
# 3️⃣ Engagement Velocity (per hour)
# -------------------------
# Group by hashtag + hour
df["hour"] = df["created_at"].dt.floor("h")  # lowercase 'h'

engagement_hourly = df.groupby(["hashtag", "hour"])[["likes", "retweets"]].sum().reset_index()
engagement_hourly["engagement"] = engagement_hourly["likes"] + engagement_hourly["retweets"]

# Map engagement per hour back to df
df = df.merge(engagement_hourly[["hashtag", "hour", "engagement"]], on=["hashtag", "hour"], how="left")

# -------------------------
# 4️⃣ Risk / Opportunity
# -------------------------
# Compute rolling mean per hashtag
rolling = engagement_hourly.groupby("hashtag").rolling(3, on="hour", min_periods=1)["engagement"].mean().reset_index()
rolling.rename(columns={"engagement": "rolling_mean_engagement"}, inplace=True)

# Merge rolling mean back
df = df.merge(rolling[["hashtag", "hour", "rolling_mean_engagement"]], on=["hashtag", "hour"], how="left")
df["opportunity_flag"] = np.where(df["engagement"] > 2 * df["rolling_mean_engagement"], "⚡ Spike", "")

# -------------------------
# 5️⃣ Optional: User Location Cleanup
# -------------------------
df["user_location"] = df["user_location"].fillna("None")

# -------------------------
# Save final CSV
# -------------------------
df.drop(columns=["hour"], inplace=True)  # keep original created_at
df.to_csv(CSV_OUTPUT, index=False, encoding="utf-8")
print(f"✅ Feature-engineered CSV saved → {CSV_OUTPUT} ({len(df)} rows)")
