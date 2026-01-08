"""
TrendPredict – Twitter/X Trend Data Ingestion
Author: Chaimaa Nairi
Description:
Fetches recent tweets for selected hashtags using Twitter/X API v2,
performs sentiment analysis, and stores results incrementally for Tableau.
"""

import tweepy
import pandas as pd
from textblob import TextBlob
from dotenv import load_dotenv
import os
import time
import requests
from urllib3.exceptions import ProtocolError
from http.client import RemoteDisconnected
from datetime import datetime

# Configuration
HASHTAGS = ["#Python", "#AI", "#DataScience"]
MAX_TWEETS_PER_HASHTAG = 20
CSV_FILE = "../data/twitter_trends.csv"
RATE_LIMIT_COOLDOWN = 5  # seconds between hashtag fetches

# Load environment variables
load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

if not BEARER_TOKEN:
    raise ValueError("❌ BEARER_TOKEN not found in environment variables")

# Authenticate with Twitter/X API v2
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True
)

# Load existing CSV (incremental ingestion)
if os.path.exists(CSV_FILE):
    df_existing = pd.read_csv(CSV_FILE)
else:
    df_existing = pd.DataFrame(columns=[
        "tweet_id",
        "created_at",
        "text",
        "likes",
        "retweets",
        "sentiment",
        "hashtag",
        "user_location"
    ])

# Safe tweet fetch function
def fetch_tweets(tag: str, since_id=None, max_tweets=20):
    """
    Fetch recent tweets for a given hashtag with robust error handling.
    """
    tweets_data = []
    query = f"{tag} -is:retweet lang:en"
    fetched = 0

    try:
        paginator = tweepy.Paginator(
            client.search_recent_tweets,
            query=query,
            tweet_fields=["created_at", "public_metrics"],
            user_fields=["location"],
            expansions=["author_id"],
            since_id=since_id,
            max_results=min(20, max_tweets)
        )

        for page in paginator:
            if not page.data:
                break

            # Map users to their locations
            users = {}
            if page.includes and "users" in page.includes:
                for user in page.includes["users"]:
                    users[user.id] = user.location

            for tweet in page.data:
                user_location = users.get(tweet.author_id)

                tweets_data.append({
                    "tweet_id": tweet.id,
                    "created_at": tweet.created_at,
                    "text": tweet.text,
                    "likes": tweet.public_metrics["like_count"],
                    "retweets": tweet.public_metrics["retweet_count"],
                    "sentiment": TextBlob(tweet.text).sentiment.polarity,
                    "hashtag": tag,
                    "user_location": user_location
                })

                fetched += 1
                if fetched >= max_tweets:
                    break

            if fetched >= max_tweets:
                break

    except tweepy.TooManyRequests:
        print(f"⚠️ Rate limit hit for {tag}. Skipping remaining fetches.")

    except (requests.exceptions.ConnectionError, ProtocolError, RemoteDisconnected) as e:
        print(f"⚠️ Network error for {tag}: {e}")

    except Exception as e:
        print(f"⚠️ Unexpected error for {tag}: {e}")

    return tweets_data

# Main execution loop
all_new_rows = []

for tag in HASHTAGS:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Fetching tweets for {tag} (up to {MAX_TWEETS_PER_HASHTAG})")

    if not df_existing.empty and tag in df_existing["hashtag"].values:
        since_id = df_existing[df_existing["hashtag"] == tag]["tweet_id"].max()
    else:
        since_id = None

    new_rows = fetch_tweets(
        tag=tag,
        since_id=since_id,
        max_tweets=MAX_TWEETS_PER_HASHTAG
    )

    print(f"[{timestamp}] Fetched {len(new_rows)} tweets for {tag}")
    all_new_rows.extend(new_rows)

    time.sleep(RATE_LIMIT_COOLDOWN)

# Save results + light cleaning
if all_new_rows:
    df_new = pd.DataFrame(all_new_rows)
    df_final = pd.concat([df_existing, df_new], ignore_index=True)

    # Remove duplicates
    df_final.drop_duplicates(subset="tweet_id", inplace=True)

    # Remove very short tweets
    df_final = df_final[df_final["text"].str.len() > 20]

    # Normalize datetime for Tableau
    df_final["created_at"] = pd.to_datetime(df_final["created_at"])
    df_final["created_at"] = df_final["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

    df_final.to_csv(CSV_FILE, index=False)
    print(f"✅ CSV updated successfully → {CSV_FILE}")
else:
    print("❌ No new data fetched. CSV not updated.")
