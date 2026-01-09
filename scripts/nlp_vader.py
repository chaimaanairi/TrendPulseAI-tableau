"""
TrendPredict – Twitter/X NLP Upgrade (VADER)
Author: Chaimaa Nairi
Description:
Reads existing Twitter/X data CSV and adds VADER sentiment analysis.
Generates sentiment_vader and sentiment_vader_category columns for Tableau dashboards.
"""

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


nltk.download('vader_lexicon')

# -------------------------
# Configuration
# -------------------------
CSV_INPUT = "../data/twitter_trends.csv"
CSV_OUTPUT = "../data/twitter_trends_vader.csv"

# -------------------------
# Load CSV
# -------------------------
df = pd.read_csv(CSV_INPUT)

# Ensure datetime format
df["created_at"] = pd.to_datetime(df["created_at"])

# -------------------------
# Initialize VADER
# -------------------------
vader = SentimentIntensityAnalyzer()

# -------------------------
# Function to compute VADER sentiment
# -------------------------
def vader_sentiment(text):
    score = vader.polarity_scores(str(text))["compound"]
    if score >= 0.05:
        category = "Positive"
    elif score <= -0.05:
        category = "Negative"
    else:
        category = "Neutral"
    return score, category

# -------------------------
# Apply VADER to all tweets
# -------------------------
vader_results = df["text"].apply(vader_sentiment)
df["sentiment_vader"] = vader_results.apply(lambda x: x[0])
df["sentiment_vader_category"] = vader_results.apply(lambda x: x[1])

# -------------------------
# Save final CSV
# -------------------------
df.to_csv(CSV_OUTPUT, index=False, encoding="utf-8")
print(f"✅ VADER-enhanced CSV saved → {CSV_OUTPUT} ({len(df)} rows)")
