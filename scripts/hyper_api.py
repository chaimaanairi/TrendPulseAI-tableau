"""
TrendPredict – Hyper API for Twitter/X Insights
Author: Chaimaa Nairi
Description:
Exposes trend, sentiment, and AI-powered recommendation metrics
via a simple API for real-time access.

- Serves aggregated trend momentum and average sentiment per hashtag.
- Provides AI recommendation per hashtag.
- Enables integration with Tableau dashboards or other apps.
- Works with existing CSVs (twitter_trends_ai.csv) for lightweight streaming/demo purposes.
"""

from fastapi import FastAPI
import pandas as pd

# -------------------------
# Initialize API
# -------------------------
app = FastAPI(title="TrendPulseAI Hyper API")

# -------------------------
# Load CSV data
# -------------------------
CSV_FILE = "../data/twitter_trends_ai.csv"
df = pd.read_csv(CSV_FILE)

# -------------------------
# Endpoint: Return aggregated trends
# -------------------------
@app.get("/trends")
def get_trends():
    """
    Returns aggregated trend metrics per hashtag:
    - Average momentum
    - Average VADER sentiment
    - Dominant AI recommendation
    """
    top_trends = df.groupby("hashtag").agg({
        "momentum": "mean",
        "sentiment_vader": "mean",
        "ai_recommendation": lambda x: x.mode()[0]  # most common recommendation
    }).reset_index()
    return top_trends.to_dict(orient="records")

# -------------------------
# Endpoint: Return AI recommendation for a specific hashtag
# -------------------------
@app.get("/recommendation/{hashtag}")
def get_recommendation(hashtag: str):
    """
    Returns the AI recommendation for a given hashtag.
    """
    data = df[df["hashtag"] == hashtag]
    if data.empty:
        return {"error": "Hashtag not found"}
    rec = data["ai_recommendation"].mode()[0]
    return {"hashtag": hashtag, "recommendation": rec}
