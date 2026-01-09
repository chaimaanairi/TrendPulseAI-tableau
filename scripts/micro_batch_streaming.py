"""
TrendPredict – Near-Real-Time Micro-Batch Streaming
Author: Chaimaa Nairi

Description:
Simulates real-time Twitter/X streaming using a micro-batch architecture.
The script periodically fetches new tweets for selected hashtags,
appends them to an existing CSV dataset, and avoids duplicates.

This approach provides near-real-time data updates without requiring
heavy streaming infrastructure (e.g., Kafka or Spark), making it
lightweight, scalable, and production-realistic.

Used for live-updating Tableau dashboards.
"""

import time
import os
import pandas as pd
from datetime import datetime

# -------------------------
# Configuration
# -------------------------
CSV_FILE = "../data/twitter_trends.csv"
REFRESH_INTERVAL = 60  # seconds (1 minute)

# -------------------------
# Simulated fetch function
# (replace with real API fetch in production)
# -------------------------
def fetch_new_tweets():
    """
    Simulates fetching new tweets.
    In production, this would call the Twitter/X API.
    """

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_data = [
        {
            "tweet_id": int(datetime.now().timestamp()),
            "created_at": now,
            "text": "Live update tweet about #AI and #Python",
            "likes": 15,
            "retweets": 7,
            "sentiment": 0.42,
            "sentiment_category": "Positive",
            "hashtag": "#AI",
            "momentum": 85.4,
            "momentum_status": "⏳ Stable",
            "user_location": "LiveStream"
        }
    ]

    return pd.DataFrame(new_data)

# -------------------------
# Micro-batch streaming loop
# -------------------------
print("🚀 Micro-batch streaming started (press CTRL+C to stop)")

while True:
    try:
        # Load existing CSV
        if os.path.exists(CSV_FILE):
            existing_df = pd.read_csv(CSV_FILE)
        else:
            existing_df = pd.DataFrame()

        # Fetch new batch
        new_df = fetch_new_tweets()

        # Avoid duplicates
        if not existing_df.empty:
            new_df = new_df[~new_df["tweet_id"].isin(existing_df["tweet_id"])]

        # Append & save
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_csv(CSV_FILE, index=False, encoding="utf-8")

        print(f"[{datetime.now().strftime('%H:%M:%S')}] CSV updated → {len(updated_df)} total rows")

        time.sleep(REFRESH_INTERVAL)

    except KeyboardInterrupt:
        print("\n🛑 Streaming stopped by user")
        break

    except Exception as e:
        print(f"⚠️ Streaming error: {e}")
        time.sleep(REFRESH_INTERVAL)