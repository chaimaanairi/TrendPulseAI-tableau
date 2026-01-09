"""
TrendPredict – Twitter/X Feature Engineering
Author: Chaimaa Nairi
Description:
Processes raw Twitter/X data (CSV) and prepares it for Tableau dashboards.
The CSV contains base metrics like likes, retweets, sentiment, and hashtag.
All advanced feature engineering (Momentum Score, Momentum Status, Engagement, Spike Detection) is implemented
directly in Tableau via calculated fields. This script ensures clean, structured CSV ready for Tableau visualization.
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
# Sentiment Category
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
# Momentum Score & Status
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
# Engagement Velocity (per hour)
# -------------------------
df["hour"] = df["created_at"].dt.floor("h")  # lowercase 'h' to avoid FutureWarning

engagement_hourly = (
    df.groupby(["hashtag", "hour"])[["likes", "retweets"]]
      .sum()
      .reset_index()
)
engagement_hourly["engagement"] = engagement_hourly["likes"] + engagement_hourly["retweets"]

# Map engagement per hour back to main df
df = df.merge(
    engagement_hourly[["hashtag", "hour", "engagement"]],
    on=["hashtag", "hour"],
    how="left"
)

# -------------------------
# Risk / Opportunity
# -------------------------
# Compute rolling mean per hashtag
rolling = (
    engagement_hourly.groupby("hashtag")
    .rolling(3, on="hour", min_periods=1)["engagement"]
    .mean()
    .reset_index()
)
rolling.rename(columns={"engagement": "rolling_mean_engagement"}, inplace=True)

# Merge rolling mean back
df = df.merge(
    rolling[["hashtag", "hour", "rolling_mean_engagement"]],
    on=["hashtag", "hour"],
    how="left"
)

# Flag spikes
df["opportunity_flag"] = np.where(
    df["engagement"] > 2 * df["rolling_mean_engagement"], "⚡ Spike", ""
)

# -------------------------
# User Location Cleanup
# -------------------------
df["user_location"] = df["user_location"].fillna("None")

# -------------------------
# Reorder Columns for Tableau
# -------------------------
columns_order = [
    "tweet_id",
    "created_at",
    "text",
    "likes",
    "retweets",
    "sentiment",
    "sentiment_category",
    "hashtag",
    "momentum_score",
    "momentum_status",
    "user_location",
    "engagement",
    "rolling_mean_engagement",
    "opportunity_flag"
]

df = df[columns_order]

# -------------------------
# Save final CSV
# -------------------------
df.to_csv(CSV_OUTPUT, index=False, encoding="utf-8")
print(f"✅ Feature-engineered CSV saved → {CSV_OUTPUT} ({len(df)} rows)")
