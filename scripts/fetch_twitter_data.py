"""
TrendPredict – Twitter/X Trend Data Ingestion (JSON)
Author: Chaimaa Nairi
Description:
Fetches recent tweets for selected hashtags using Twitter/X API v2,
performs sentiment analysis, calculates momentum metrics, and
stores results incrementally as JSON for Tableau.
"""

import tweepy
import json
from textblob import TextBlob
from dotenv import load_dotenv
import os
import time
import requests
from urllib3.exceptions import ProtocolError
from http.client import RemoteDisconnected
from datetime import datetime

# -------------------------
# Configuration
# -------------------------
HASHTAGS = ["#Python", "#AI", "#DataScience"]
MAX_TWEETS_PER_HASHTAG = 50
JSON_FILE = "../data/twitter_trends.json"
RATE_LIMIT_COOLDOWN = 5  # seconds between hashtag fetches

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
if not BEARER_TOKEN:
    raise ValueError("❌ BEARER_TOKEN not found in environment variables")

# -------------------------
# Authenticate with Twitter/X API v2
# -------------------------
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

# -------------------------
# Helper functions
# -------------------------
def get_sentiment_category(sentiment):
    if sentiment < -0.1:
        return "Negative"
    elif sentiment <= 0.1:
        return "Neutral"
    else:
        return "Positive"

def get_momentum_score(likes, retweets, sentiment):
    return round((likes + retweets) * 0.7 + sentiment * 0.3 * 100, 2)

def get_momentum_status(score):
    if score >= 400:
        return "🔥 Exploding"
    elif score >= 200:
        return "🚀 Emerging"
    else:
        return "⏳ Stable"

# -------------------------
# Fetch tweets safely
# -------------------------
def fetch_tweets(tag: str, since_id=None, max_tweets=50):
    all_data = []
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
                    users[user.id] = user.location if user.location else "None"

            for tweet in page.data:
                likes = tweet.public_metrics["like_count"]
                retweets = tweet.public_metrics["retweet_count"]
                sentiment = round(TextBlob(tweet.text).sentiment.polarity, 3)
                sentiment_category = get_sentiment_category(sentiment)
                momentum = get_momentum_score(likes, retweets, sentiment)
                momentum_status = get_momentum_status(momentum)
                user_location = users.get(tweet.author_id, "None")

                all_data.append({
                    "tweet_id": tweet.id,
                    "created_at": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "text": tweet.text,
                    "likes": likes,
                    "retweets": retweets,
                    "sentiment": sentiment,
                    "sentiment_category": sentiment_category,
                    "hashtag": tag,
                    "momentum": momentum,
                    "momentum_status": momentum_status,
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

    return all_data

# -------------------------
# Main execution loop
# -------------------------
all_new_rows = []

for tag in HASHTAGS:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Fetching tweets for {tag} (up to {MAX_TWEETS_PER_HASHTAG})")

    # Determine the latest tweet_id for incremental fetch
    since_id = None
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            tag_ids = [t["tweet_id"] for t in existing_data if t["hashtag"] == tag]
            if tag_ids:
                since_id = max(tag_ids)
        except Exception:
            since_id = None

    new_rows = fetch_tweets(tag=tag, since_id=since_id, max_tweets=MAX_TWEETS_PER_HASHTAG)
    all_new_rows.extend(new_rows)

    print(f"[{timestamp}] Fetched {len(new_rows)} tweets for {tag}")
    time.sleep(RATE_LIMIT_COOLDOWN)

# -------------------------
# Save JSON results
# -------------------------
final_data = []

# Load existing JSON if present
if os.path.exists(JSON_FILE):
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            final_data = json.load(f)
    except Exception:
        final_data = []

# Append new rows
final_data.extend(all_new_rows)

# Remove duplicates by tweet_id
unique_data = {item["tweet_id"]: item for item in final_data}
final_data = list(unique_data.values())

# Save JSON
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"✅ JSON updated successfully → {JSON_FILE} ({len(final_data)} total tweets)")
