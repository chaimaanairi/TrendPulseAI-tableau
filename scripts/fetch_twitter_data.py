import tweepy
import pandas as pd
from textblob import TextBlob
from dotenv import load_dotenv
import os
import time

# -------------------------
# 1️⃣ Load environment variables
# -------------------------
load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# -------------------------
# 2️⃣ Authenticate with Twitter/X v2
# -------------------------
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

# -------------------------
# 3️⃣ Define hashtags to track
# -------------------------
hashtags = ["#Python", "#AI", "#DataScience"]  # choose which to fetch per demo

# -------------------------
# 4️⃣ CSV setup
# -------------------------
csv_file = "../data/twitter_trends.csv"
if os.path.exists(csv_file):
    df_existing = pd.read_csv(csv_file)
else:
    df_existing = pd.DataFrame(columns=[
        "tweet_id", "created_at", "text", "likes", "retweets", "sentiment", "hashtag"
    ])

# -------------------------
# 5️⃣ Fetch only new tweets for each hashtag
# -------------------------
all_new_data = []

for tag in hashtags:
    print(f"Fetching new tweets for {tag}...")

    # Find the newest tweet ID already fetched for this hashtag
    if not df_existing.empty and tag in df_existing["hashtag"].values:
        max_id = df_existing[df_existing["hashtag"] == tag]["tweet_id"].max()
    else:
        max_id = None  # fetch most recent tweets if none exist

    query = f"{tag} -is:retweet lang:en"

    try:
        for tweet in tweepy.Paginator(
            client.search_recent_tweets,
            query=query,
            tweet_fields=["created_at", "public_metrics"],
            since_id=max_id,
            max_results=50
        ).flatten(limit=50):  # fetch up to 50 new tweets
            all_new_data.append({
                "tweet_id": tweet.id,
                "created_at": tweet.created_at,
                "text": tweet.text,
                "likes": tweet.public_metrics["like_count"],
                "retweets": tweet.public_metrics["retweet_count"],
                "sentiment": TextBlob(tweet.text).sentiment.polarity,
                "hashtag": tag
            })

        print(f"Fetched {len(all_new_data)} new tweets for {tag} ✅")
        time.sleep(5)  # small pause to avoid hitting rate limits

    except tweepy.TooManyRequests as e:
        reset_time = int(e.response.headers.get("x-rate-limit-reset", time.time() + 60))
        wait_seconds = max(reset_time - int(time.time()), 60)
        print(f"Rate limit reached for {tag}. Sleeping for {wait_seconds} seconds...")
        time.sleep(wait_seconds)

# -------------------------
# 6️⃣ Save incremental CSV
# -------------------------
if all_new_data:
    df_new = pd.DataFrame(all_new_data)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_csv(csv_file, index=False)
    print(f"{csv_file} updated with new tweets ✅")
else:
    print("No new tweets fetched this run.")
